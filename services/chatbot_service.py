import json
from models import (
    FarmModel, CropModel, ObservationModel, AgentRunModel,
    RecommendationModel, MemoryModel, ChatModel, QuickNoteModel
)
from services.groq_service import GroqService

from services.language_service import LanguageService

class ChatbotService:
    @staticmethod
    def get_context_payload(user_id):
        """Assemble current farm telemetry, crop data, agent outputs, memories, and recommendations."""
        try:
            farm = FarmModel.get_by_user_id(user_id)
            if not isinstance(farm, dict):
                farm = None
        except Exception:
            farm = None

        farm_id = farm['id'] if farm else None
        
        try:
            crop = CropModel.get_by_farm_id(farm_id) if farm_id else None
            if not isinstance(crop, dict):
                crop = None
        except Exception:
            crop = None

        try:
            observation = ObservationModel.get_latest(farm_id) if farm_id else None
            if not isinstance(observation, dict):
                observation = None
        except Exception:
            observation = None

        try:
            recommendations = RecommendationModel.get_active(farm_id) if farm_id else []
            if not isinstance(recommendations, list):
                recommendations = []
        except Exception:
            recommendations = []

        try:
            memories = MemoryModel.get_recent(farm_id, limit=3) if farm_id else []
            if not isinstance(memories, list):
                memories = []
        except Exception:
            memories = []
        
        try:
            quick_notes = QuickNoteModel.get_incomplete_by_user(user_id)
            if not isinstance(quick_notes, list):
                quick_notes = []
        except Exception:
            quick_notes = []

        # Get latest run result for each agent
        agent_names = [
            'Weather Agent', 'Soil Agent', 'Crop Disease Agent',
            'Market Agent', 'Irrigation Agent', 'Fertilizer Agent', 'Farm Planning Agent'
        ]
        agent_runs = {}
        for name in agent_names:
            agent_runs[name] = None

        if farm_id:
            for name in agent_names:
                try:
                    run = AgentRunModel.get_latest_by_agent(farm_id, name)
                    if isinstance(run, dict) and run.get('output_json'):
                        try:
                            agent_runs[name] = json.loads(run['output_json'])
                        except:
                            agent_runs[name] = run['output_json']
                except Exception:
                    pass

        return {
            "farm": farm,
            "crop": crop,
            "observation": observation,
            "recommendations": recommendations,
            "memories": memories,
            "agent_runs": agent_runs,
            "quick_notes": quick_notes
        }

    @staticmethod
    def generate_reply(user_id, message, language='en'):
        """Produce the chatbot answer using Gemini and the user's farm context."""
        try:
            farm = FarmModel.get_by_user_id(user_id)
            if not isinstance(farm, dict):
                farm = None
        except Exception:
            farm = None

        farm_id = farm['id'] if farm else None
        
        # Save user message to database
        try:
            ChatModel.add_message(user_id, farm_id, 'user', message, language)
        except Exception:
            pass

        # Load context
        ctx = ChatbotService.get_context_payload(user_id)
        if not isinstance(ctx, dict):
            ctx = {}
        
        language_name = LanguageService.get_language_name(language)

        # Formulate prompt text with agricultural data context
        context_str = ""
        
        # 1. Farm Info
        farm_info = ctx.get('farm')
        if isinstance(farm_info, dict):
            context_str += f"=== FARM INFO ===\n"
            context_str += f"Name: {farm_info.get('name') or 'N/A'}\n"
            context_str += f"Location: {farm_info.get('location') or 'N/A'}\n"
            context_str += f"Area: {farm_info.get('area') or 'N/A'} acres\n"
            context_str += f"Soil Type: {farm_info.get('soil_type') or 'N/A'}\n"
            context_str += f"Irrigation Method: {farm_info.get('irrigation_method') or 'N/A'}\n\n"
        else:
            context_str += "=== FARM INFO ===\nNo farm has been configured yet.\n\n"

        # 2. Crop Info
        crop_info = ctx.get('crop')
        if isinstance(crop_info, dict):
            context_str += f"=== CROP INFO ===\n"
            context_str += f"Name: {crop_info.get('name') or 'N/A'}\n"
            context_str += f"Variety: {crop_info.get('variety') or 'N/A'}\n"
            context_str += f"Stage: {crop_info.get('stage') or 'N/A'}\n"
            context_str += f"Planting Date: {crop_info.get('planting_date') or 'N/A'}\n\n"

        # 3. Observation Telemetry
        obs = ctx.get('observation')
        if isinstance(obs, dict):
            context_str += f"=== LATEST TELEMETRY OBSERVATION ===\n"
            context_str += f"Moisture: {obs.get('soil_moisture') or 0}%, pH: {obs.get('soil_ph') or 7.0}\n"
            context_str += f"N-P-K: {obs.get('nitrogen') or 0}-{obs.get('phosphorus') or 0}-{obs.get('potassium') or 0} kg/ha\n"
            context_str += f"Temp: {obs.get('temperature') or 0}°C, Humidity: {obs.get('humidity') or 0}%, Rainfall: {obs.get('rainfall') or 0}mm\n"
            context_str += f"Crop Health Index: {obs.get('crop_health') or 0}%\n"
            context_str += f"Disease Notes: {obs.get('disease_notes') or 'None'}\n"
            context_str += f"Mandi Price: {obs.get('market_price') or 0.0} INR/quintal\n\n"

        # 4. Agent Recommendations
        recs = ctx.get('recommendations')
        if isinstance(recs, list) and recs:
            context_str += f"=== ACTIVE AGENT RECOMMENDATIONS ===\n"
            for r in recs:
                if isinstance(r, dict):
                    context_str += f"- [{r.get('agent_name') or 'Agent'}] {r.get('title') or 'Rec'}: {r.get('description') or ''} (Priority: {r.get('priority') or 'Medium'})\n"
            context_str += "\n"

        # 5. Agent Runs Context
        agent_names = [
            'Weather Agent', 'Soil Agent', 'Crop Disease Agent',
            'Market Agent', 'Irrigation Agent', 'Fertilizer Agent', 'Farm Planning Agent'
        ]
        context_str += f"=== LATEST RUNS FOR AGENTS ===\n"
        agent_runs = ctx.get('agent_runs') or {}
        for name in agent_names:
            out = agent_runs.get(name) if isinstance(agent_runs, dict) else None
            if out is None:
                context_str += f"- {name}: I don't have a recent analysis from that agent yet.\n"
            elif isinstance(out, dict):
                sum_val = out.get('summary') or out.get('final_plan') or out.get('recommendation') or out.get('final_farm_plan') or ''
                if not sum_val:
                    sum_val = "I don't have a recent analysis from that agent yet."
                context_str += f"- {name}: {sum_val}\n"
            else:
                context_str += f"- {name}: {out}\n"
        context_str += "\n"

        # 6. Farm Memory
        mems = ctx.get('memories')
        if isinstance(mems, list) and mems:
            context_str += f"=== RECENT FARM MEMORIES ===\n"
            for m in mems:
                if isinstance(m, dict):
                    context_str += f"- {m.get('plan_summary') or 'Plan'} (Risk Assessment: {m.get('risk_assessment') or 'N/A'})\n"
            context_str += "\n"

        # 7. Quick Notes (Shopping Checklist)
        qnotes = ctx.get('quick_notes')
        context_str += f"=== FARM QUICK NOTES (SHOPPING CHECKLIST) ===\n"
        if isinstance(qnotes, list) and qnotes:
            context_str += "The farmer has saved the following active/incomplete farm items to buy:\n"
            for note in qnotes:
                if isinstance(note, dict):
                    context_str += f"- {note.get('note') or ''}\n"
            context_str += "\n"
        else:
            context_str += "You don't have any active farm quick notes.\n\n"

        system_instruction = (
            "You are KisanMitra AI, an intelligent digital farm companion.\n"
            "You help farmers understand their farm data and the recommendations produced by the Autonomous AI Farmer system.\n"
            "Use the supplied farm context when answering.\n"
            "Never invent missing measurements, weather information, market prices, disease diagnoses, or agricultural observations.\n"
            "Clearly communicate uncertainty.\n"
            "When farm information is unavailable, say that the required data is unavailable.\n"
            "Do not claim to have live information unless live information has actually been provided by the application.\n"
            "Provide practical, understandable answers.\n"
            "You can explain the outputs of the farming agents, but you must not fabricate agent results.\n"
            "When the user asks 'What do I need to buy?' or asks about their quick notes/shopping list, you must retrieve and state only the items listed in the === FARM QUICK NOTES === section. Never fabricate or invent any shopping checklist items.\n"
            "If the context states 'I don't have a recent analysis from that agent yet.' for any agent, and the user asks about that agent's status or results, you must respond with: 'I don't have a recent analysis from that agent yet.' (or the equivalent in the user's selected language).\n"
            "If the context states 'You don't have any active farm quick notes.', and the user asks about their checklist, shopping list, or what they need to buy, you must respond with: 'You don't have any active farm quick notes.' (or the equivalent in the user's selected language).\n"
            "For potentially serious crop disease or agricultural decisions, recommend appropriate local agricultural expertise when the available information is insufficient.\n"
            f"CRITICAL: Always respond in the user's selected language: {language_name}.\n"
            f"If the selected language is Telugu, write the entire reply only in Telugu script (తెలుగు). "
            f"If Hindi, use Devanagari script. If Tamil, use Tamil script. If Kannada, use Kannada script. "
            f"If Japanese, use Japanese (Hiragana/Katakana/Kanji). If Korean, use Korean (Hangul). "
            f"Never mix languages — respond exclusively in the requested language."
        )

        prompt = (
            f"User selected language: {language_name}\n\n"
            f"{context_str}"
            f"User Question:\n{message}"
        )

        try:
            # Generate response from Groq
            reply = GroqService.generate_response(prompt=prompt, system_instruction=system_instruction, lang_code=language)
            if not reply or "is not configured" in reply or "invocation failed" in reply:
                from config import Config
                if not Config.GROQ_API_KEY:
                    reply = "AI service is not configured. Please check the server configuration."
                else:
                    reply = "Sorry, I couldn't process that right now. Please try again."
        except Exception:
            reply = "Sorry, I couldn't process that right now. Please try again."

        # Save assistant message to database
        try:
            ChatModel.add_message(user_id, farm_id, 'assistant', reply, language)
        except Exception:
            pass
            
        return reply
