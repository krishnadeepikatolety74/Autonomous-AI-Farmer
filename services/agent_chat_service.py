import json
from models import (
    FarmModel, CropModel, ObservationModel, AgentRunModel,
    RecommendationModel, MemoryModel, AgentChatModel, QuickNoteModel
)
from services.gemini_service import GeminiService
from services.weather_service import WeatherService

# Import prompt definitions
from agents.prompts.weather_prompt import SYSTEM_PROMPT as weather_instruction
from agents.prompts.soil_prompt import SYSTEM_PROMPT as soil_instruction
from agents.prompts.disease_prompt import SYSTEM_PROMPT as disease_instruction
from agents.prompts.irrigation_prompt import SYSTEM_PROMPT as irrigation_instruction
from agents.prompts.fertilizer_prompt import SYSTEM_PROMPT as fertilizer_instruction
from agents.prompts.market_prompt import SYSTEM_PROMPT as market_instruction
from agents.prompts.planning_prompt import SYSTEM_PROMPT as planning_instruction

from services.language_service import LanguageService

PROMPT_MAP = {
    'weather': (weather_instruction, 'Weather Agent'),
    'soil': (soil_instruction, 'Soil Agent'),
    'crop-disease': (disease_instruction, 'Crop Disease Agent'),
    'irrigation': (irrigation_instruction, 'Irrigation Agent'),
    'fertilizer': (fertilizer_instruction, 'Fertilizer Agent'),
    'market': (market_instruction, 'Market Agent'),
    'farm-planning': (planning_instruction, 'Farm Planning Agent')
}

class AgentChatService:
    @staticmethod
    def get_agent_context(user_id, agent_slug):
        """Assemble specific scoped farm context for the chosen agent slug."""
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
            obs = ObservationModel.get_latest(farm_id) if farm_id else None
            if not isinstance(obs, dict):
                obs = None
        except Exception:
            obs = None

        # Scope context to agent
        if agent_slug == 'weather':
            location = farm.get('location', 'India') if farm else 'India'
            live = WeatherService.fetch_live_weather(location)
            live_avail = live is not None
            if live_avail:
                weather_str = (
                    f"Resolved Location: {live['location']}\n"
                    f"Condition: {live['condition']}\n"
                    f"Temperature: {live['temperature_c']}°C (feels like {live['feels_like_c']}°C)\n"
                    f"Humidity: {live['humidity_pct']}%\n"
                    f"Precipitation: {live['precipitation_mm']} mm\n"
                    f"Wind Speed: {live['wind_speed_kmh']} km/h\n"
                    f"UV Index: {live['uv_index']}\n"
                )
            elif obs:
                weather_str = (
                    f"Temperature: {obs.get('temperature', 24.0)}°C\n"
                    f"Humidity: {obs.get('humidity', 68.0)}%\n"
                    f"Rainfall: {obs.get('rainfall', 10.0)} mm\n"
                )
            else:
                weather_str = "No weather data available.\n"
                
            crop_str = f"Crop: {crop.get('name', 'Wheat')} (Stage: {crop.get('stage', 'Vegetative')})\n" if crop else "No crop registered.\n"
            return f"=== WEATHER INFO ===\n{weather_str}\n=== CROP INFO ===\n{crop_str}"

        elif agent_slug == 'soil':
            if obs:
                soil_str = (
                    f"Soil Moisture: {obs.get('soil_moisture') or 0}%\n"
                    f"Soil pH: {obs.get('soil_ph') or 7.0}\n"
                    f"Nitrogen (N): {obs.get('nitrogen') or 0} kg/ha\n"
                    f"Phosphorus (P): {obs.get('phosphorus') or 0} kg/ha\n"
                    f"Potassium (K): {obs.get('potassium') or 0} kg/ha\n"
                )
            else:
                soil_str = "No soil telemetry available.\n"
            
            farm_str = f"Soil Type: {farm.get('soil_type', 'Loamy')}\n" if farm else ""
            crop_str = f"Crop: {crop.get('name', 'Wheat')} (Stage: {crop.get('stage', 'Vegetative')})\n" if crop else ""
            return f"=== SOIL TELEMETRY ===\n{soil_str}{farm_str}\n=== CROP INFO ===\n{crop_str}"

        elif agent_slug == 'crop-disease':
            if obs:
                disease_str = (
                    f"Crop Health Index: {obs.get('crop_health') or 0}%\n"
                    f"Observed Symptoms/Notes: {obs.get('disease_notes') or 'None'}\n"
                    f"Temperature: {obs.get('temperature', 24.0)}°C, Humidity: {obs.get('humidity', 68.0)}%\n"
                )
            else:
                disease_str = "No disease telemetry available.\n"
            crop_str = f"Crop: {crop.get('name', 'Wheat')} (Variety: {crop.get('variety', 'Standard')}, Stage: {crop.get('stage', 'Vegetative')})\n" if crop else ""
            
            from flask import has_request_context, session
            analysis_str = ""
            if has_request_context():
                latest_analysis = session.get('last_crop_analysis')
                if latest_analysis:
                    analysis_str = f"\n=== LATEST IMAGE ANALYSIS RESULT ===\n{json.dumps(latest_analysis, indent=2)}\n"
            
            return f"=== CROP HEALTH & SYMPTOMS ===\n{disease_str}\n=== CROP INFO ===\n{crop_str}{analysis_str}"

        elif agent_slug == 'irrigation':
            if obs:
                irr_str = (
                    f"Soil Moisture: {obs.get('soil_moisture') or 0}%\n"
                    f"Rainfall: {obs.get('rainfall', 0.0)} mm\n"
                    f"Temperature: {obs.get('temperature', 24.0)}°C\n"
                )
            else:
                irr_str = "No irrigation telemetry available.\n"
            farm_str = f"Irrigation Method: {farm.get('irrigation_method', 'Drip')}, Soil Type: {farm.get('soil_type', 'Loamy')}\n" if farm else ""
            crop_str = f"Crop Stage: {crop.get('stage', 'Vegetative')}\n" if crop else ""
            return f"=== IRRIGATION ENVIRONMENT ===\n{irr_str}{farm_str}\n=== CROP INFO ===\n{crop_str}"

        elif agent_slug == 'fertilizer':
            if obs:
                fert_str = (
                    f"Nitrogen (N): {obs.get('nitrogen') or 0} kg/ha\n"
                    f"Phosphorus (P): {obs.get('phosphorus') or 0} kg/ha\n"
                    f"Potassium (K): {obs.get('potassium') or 0} kg/ha\n"
                    f"Soil pH: {obs.get('soil_ph') or 7.0}\n"
                )
            else:
                fert_str = "No nutrient data available.\n"
            crop_str = f"Crop: {crop.get('name', 'Wheat')} (Variety: {crop.get('variety', 'Standard')}, Stage: {crop.get('stage', 'Vegetative')})\n" if crop else ""
            return f"=== SOIL NUTRIENTS (NPK) ===\n{fert_str}\n=== CROP INFO ===\n{crop_str}"

        elif agent_slug == 'market':
            if obs:
                mkt_str = f"Farmer-provided Market Price: {obs.get('market_price') or 0.0} INR/quintal\n"
            else:
                mkt_str = "No market price registered in farm profile yet.\n"
            crop_str = f"Crop: {crop.get('name', 'Wheat')} (Variety: {crop.get('variety', 'Standard')}, Stage: {crop.get('stage', 'Vegetative')})\n" if crop else ""
            return f"=== MARKET PRICES ===\n{mkt_str}\n=== CROP INFO ===\n{crop_str}"

        elif agent_slug == 'farm-planning':
            parts = []
            if farm:
                parts.append(f"=== FARM INFO ===\nName: {farm.get('name')}, Location: {farm.get('location')}, Soil Type: {farm.get('soil_type')}, Area: {farm.get('area')} acres\n")
            if crop:
                parts.append(f"=== CROP INFO ===\nName: {crop.get('name')}, Variety: {crop.get('variety')}, Stage: {crop.get('stage')}\n")
            if obs:
                parts.append(f"=== LATEST TELEMETRY ===\nMoisture: {obs.get('soil_moisture')}%, pH: {obs.get('soil_ph')}, NPK: {obs.get('nitrogen')}-{obs.get('phosphorus')}-{obs.get('potassium')} kg/ha, Temp: {obs.get('temperature')}°C, Rainfall: {obs.get('rainfall')}mm, Crop Health: {obs.get('crop_health')}%")
                
            try:
                recs = RecommendationModel.get_active(farm_id) if farm_id else []
                if recs:
                    parts.append("=== ACTIVE AGENT RECOMMENDATIONS ===")
                    for r in recs:
                        parts.append(f"- [{r.get('agent_name')}] {r.get('title')}: {r.get('description')} (Priority: {r.get('priority')})")
            except Exception:
                pass
                
            agent_names = [
                'Weather Agent', 'Soil Agent', 'Crop Disease Agent',
                'Market Agent', 'Irrigation Agent', 'Fertilizer Agent', 'Farm Planning Agent'
            ]
            parts.append("=== LATEST RUNS FOR AGENTS ===")
            for name in agent_names:
                try:
                    run = AgentRunModel.get_latest_by_agent(farm_id, name) if farm_id else None
                    if run and run.get('output_json'):
                        out_json = json.loads(run['output_json']) if isinstance(run['output_json'], str) else run['output_json']
                        sum_val = out_json.get('summary') or out_json.get('final_plan') or out_json.get('recommendation') or out_json.get('final_farm_plan') or ''
                        if not sum_val:
                            sum_val = "I don't have a recent analysis from that agent yet."
                        parts.append(f"- {name}: {sum_val}")
                    else:
                        parts.append(f"- {name}: I don't have a recent analysis from that agent yet.")
                except Exception:
                    parts.append(f"- {name}: I don't have a recent analysis from that agent yet.")
                    
            try:
                mems = MemoryModel.get_recent(farm_id, limit=3) if farm_id else []
                if mems:
                    parts.append("=== RECENT FARM MEMORIES ===")
                    for m in mems:
                        parts.append(f"- {m.get('plan_summary')} (Risk Assessment: {m.get('risk_assessment')})")
            except Exception:
                pass
                
            try:
                qnotes = QuickNoteModel.get_incomplete_by_user(user_id)
                parts.append("=== FARM QUICK NOTES ===")
                if qnotes:
                    for note in qnotes:
                        parts.append(f"- {note.get('note')}")
                else:
                    parts.append("You don't have any active farm quick notes.")
            except Exception:
                pass
                
            return "\n".join(parts)
            
        return "No context available."

    @classmethod
    def generate_reply(cls, user_id, agent_slug, message, language='en'):
        """Produce the agent-specific chatbot answer using Gemini and correct domain prompts."""
        if agent_slug not in PROMPT_MAP:
            raise ValueError(f"Unknown agent slug: {agent_slug}")

        try:
            farm = FarmModel.get_by_user_id(user_id)
            if not isinstance(farm, dict):
                farm = None
        except Exception:
            farm = None

        farm_id = farm['id'] if farm else None
        
        system_instruction_tpl, agent_name = PROMPT_MAP[agent_slug]

        # 1. Save user message to database
        try:
            AgentChatModel.add_message(user_id, farm_id, agent_name, 'user', message, language)
        except Exception:
            pass

        # 2. Prepare Context
        ctx_str = cls.get_agent_context(user_id, agent_slug)
        language_name = LanguageService.get_language_name(language)

        # 3. Format system instruction
        system_instruction = system_instruction_tpl.format(context=ctx_str, language_name=language_name)

        prompt = (
            f"User selected language: {language_name}\n\n"
            f"User Question:\n{message}"
        )

        try:
            # Generate response from Gemini
            reply = GeminiService.generate_response(prompt=prompt, system_instruction=system_instruction, lang_code=language)
            if not reply or reply == "AI service temporarily unavailable.":
                from config import Config
                if not Config.GEMINI_API_KEY:
                    reply = "AI service is not configured. Please check the server configuration."
                else:
                    reply = "AI service is temporarily unavailable. Please try again."
        except Exception:
            reply = "AI service is temporarily unavailable. Please try again."

        # 4. Save assistant message to database
        try:
            AgentChatModel.add_message(user_id, farm_id, agent_name, 'assistant', reply, language)
        except Exception:
            pass

        return reply
