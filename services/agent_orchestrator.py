import datetime
import json
from agents import (
    WeatherAgent, SoilAgent, DiseaseAgent, MarketAgent,
    IrrigationAgent, FertilizerAgent, FarmPlanningAgent
)
from models import AgentRunModel, RecommendationModel, MemoryModel

class AgentOrchestrator:
    @staticmethod
    def run_all(farm, crop, observation, user_id=None):
        """
        Execute all agents sequentially in a chain and save execution details,
        recommendations and memory records to SQLite.
        """
        farm_id = farm['id']
        
        # Instantiate agents
        weather_agent = WeatherAgent()
        soil_agent = SoilAgent()
        disease_agent = DiseaseAgent()
        market_agent = MarketAgent()
        irrigation_agent = IrrigationAgent()
        fertilizer_agent = FertilizerAgent()
        coordinator = FarmPlanningAgent()

        results = {}
        
        # 1. Weather Agent
        run_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        w_res = weather_agent.run(farm, crop, observation)
        results['Weather Agent'] = w_res
        AgentOrchestrator._record_run(farm_id, 'Weather Agent', w_res, run_time)

        # 2. Soil Agent
        run_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        s_res = soil_agent.run(farm, crop, observation)
        results['Soil Agent'] = s_res
        AgentOrchestrator._record_run(farm_id, 'Soil Agent', s_res, run_time)

        # 3. Crop Disease Agent
        run_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        d_res = disease_agent.run(farm, crop, observation)
        results['Crop Disease Agent'] = d_res
        AgentOrchestrator._record_run(farm_id, 'Crop Disease Agent', d_res, run_time)

        # 4. Market Agent
        run_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        m_res = market_agent.run(farm, crop, observation)
        results['Market Agent'] = m_res
        AgentOrchestrator._record_run(farm_id, 'Market Agent', m_res, run_time)

        # 5. Irrigation Agent (Receives Weather and Soil details)
        run_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        i_res = irrigation_agent.run(farm, crop, observation, previous_results=results)
        results['Irrigation Agent'] = i_res
        AgentOrchestrator._record_run(farm_id, 'Irrigation Agent', i_res, run_time)

        # 6. Fertilizer Agent (Receives Soil details)
        run_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f_res = fertilizer_agent.run(farm, crop, observation, previous_results=results)
        results['Fertilizer Agent'] = f_res
        AgentOrchestrator._record_run(farm_id, 'Fertilizer Agent', f_res, run_time)

        # Get recent memory timeline context
        recent_memories = MemoryModel.get_recent(farm_id, limit=3)
        memory_str = json.dumps(recent_memories)

        # 7. Farm Planning Agent (Coordinator - Receives all outputs + memory)
        run_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        coord_res = coordinator.run(farm, crop, observation, previous_results=results, memory_context=memory_str)
        results['Farm Planning Agent'] = coord_res
        AgentOrchestrator._record_run(farm_id, 'Farm Planning Agent', coord_res, run_time)

        # Process Coordinator results into final plan recommendations
        if 'error' not in coord_res:
            overall_status = coord_res.get('overall_status', 'Good')
            overall_risk = coord_res.get('overall_risk', 'Low')
            summary = coord_res.get('summary', 'Plan updated.')
            final_plan = coord_res.get('final_plan', '')
            
            # Save to Farm Memory timeline
            MemoryModel.add(farm_id, summary, f"Status: {overall_status}, Risk: {overall_risk}. Plan: {final_plan}")
            
            # Process sub-agent and coordinator actions into recommendations table
            # First, clear previous uncompleted recommendations
            for agent_name in results.keys():
                RecommendationModel.clear_active_by_agent(farm_id, agent_name)

            # Insert new recommendations from coordinator priority_actions list
            priority_actions = coord_res.get('priority_actions', [])
            for action in priority_actions:
                act_agent = action.get('agent', 'Farm Planning Agent')
                title = action.get('title', 'Action Required')
                desc = action.get('description', '')
                priority = action.get('priority', 'Medium')
                RecommendationModel.create(farm_id, act_agent, title, desc, priority)

            # If coordinator didn't return any actions, pull from individual sub-agent recommendations
            if not priority_actions:
                for agent_name, agent_out in results.items():
                    if agent_name == 'Farm Planning Agent':
                        continue
                    actions = agent_out.get('actions', [])
                    for act in actions:
                        RecommendationModel.create(
                            farm_id,
                            agent_name,
                            act.get('title', 'Action Required'),
                            act.get('description', ''),
                            act.get('priority', 'Medium')
                        )

            # Trigger Smart Alerts based on observation thresholds and recommendations
            try:
                from services.alert_service import AlertService
                obs_dict = dict(observation) if observation else {}
                active_recs = RecommendationModel.get_active(farm_id)
                rec_list = [dict(r) for r in active_recs] if active_recs else []
                AlertService.check_and_generate_alerts(farm_id, obs_dict, rec_list)
            except Exception as e:
                print(f"Alert generation warning: {e}")

            # Auto-generate Calendar Tasks from new recommendations
            try:
                from services.calendar_service import CalendarService
                target_uid = user_id or farm.get('user_id')
                if target_uid:
                    active_recs = RecommendationModel.get_active(farm_id)
                    rec_list = [dict(r) for r in active_recs] if active_recs else []
                    CalendarService.generate_tasks_from_recommendations(target_uid, farm_id, rec_list)
            except Exception as e:
                print(f"Calendar task generation warning: {e}")

        return results

    @staticmethod
    def run_single(farm, crop, observation, agent_name):
        """Execute a single agent and update recommendations/runs database logs."""
        farm_id = farm['id']
        run_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Instantiate agent mapping
        agents_map = {
            'Weather Agent': WeatherAgent,
            'Soil Agent': SoilAgent,
            'Crop Disease Agent': DiseaseAgent,
            'Market Agent': MarketAgent,
            'Irrigation Agent': IrrigationAgent,
            'Fertilizer Agent': FertilizerAgent,
            'Farm Planning Agent': FarmPlanningAgent
        }
        
        if agent_name not in agents_map:
            raise ValueError(f"Unknown agent: {agent_name}")
            
        agent = agents_map[agent_name]()
        
        # Pull outputs of other agents to serve as mock context if needed
        # (Irrigation / Fertilizer / Coordinator require some context)
        other_results = {}
        for other_name in agents_map.keys():
            if other_name == agent_name:
                continue
            latest_run = AgentRunModel.get_latest_by_agent(farm_id, other_name)
            if latest_run and latest_run.get('output_json'):
                try:
                    other_results[other_name] = json.loads(latest_run['output_json'])
                except:
                    pass

        # Execute
        if agent_name == 'Farm Planning Agent':
            recent_memories = MemoryModel.get_recent(farm_id, limit=3)
            memory_str = json.dumps(recent_memories)
            res = agent.run(farm, crop, observation, previous_results=other_results, memory_context=memory_str)
        else:
            res = agent.run(farm, crop, observation, previous_results=other_results)
            
        AgentOrchestrator._record_run(farm_id, agent_name, res, run_time)
        
        # If successfully executed, clear uncompleted recommendations from this agent and create new ones
        if 'error' not in res:
            RecommendationModel.clear_active_by_agent(farm_id, agent_name)
            
            # If it is the coordinator, update the farm memory and priority actions
            if agent_name == 'Farm Planning Agent':
                overall_status = res.get('overall_status', 'Good')
                overall_risk = res.get('overall_risk', 'Low')
                summary = res.get('summary', 'Plan updated.')
                final_plan = res.get('final_plan', '')
                MemoryModel.add(farm_id, summary, f"Status: {overall_status}, Risk: {overall_risk}. Plan: {final_plan}")
                
                priority_actions = res.get('priority_actions', [])
                for action in priority_actions:
                    RecommendationModel.create(
                        farm_id,
                        action.get('agent', 'Farm Planning Agent'),
                        action.get('title', 'Action Required'),
                        action.get('description', ''),
                        action.get('priority', 'Medium')
                    )
            else:
                # Add action tasks returned from individual sub-agent
                actions = res.get('actions', [])
                for act in actions:
                    RecommendationModel.create(
                        farm_id,
                        agent_name,
                        act.get('title', 'Action Required'),
                        act.get('description', ''),
                        act.get('priority', 'Medium')
                    )
                    
        return res

    @staticmethod
    def _record_run(farm_id, agent_name, output_json, run_time):
        """Helper to write run metrics to database."""
        status = "Failed" if "error" in output_json else "Completed"
        risk_level = output_json.get('risk_level', output_json.get('overall_risk', 'Low'))
        confidence = output_json.get('confidence', 90.0)
        
        AgentRunModel.record(
            farm_id=farm_id,
            agent_name=agent_name,
            status=status,
            risk_level=risk_level,
            confidence=confidence,
            run_time=run_time,
            output_json=json.dumps(output_json)
        )
