from .base_agent import BaseAgent
from services.gemini_service import GeminiService

class IrrigationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Irrigation Agent",
            description="Optimizes water distribution grids and sets daily irrigation schedules."
        )

    def run(self, farm, crop, observation, previous_results=None, memory_context=None):
        system_instruction = (
            "You are an expert Irrigation Engineer AI Agent. Optimize farm water management "
            "and suggest irrigation schedules in strict JSON format."
        )
        
        # Prepare inputs from dependencies (Weather + Soil outputs)
        weather_out = previous_results.get('Weather Agent', {}) if previous_results else {}
        soil_out = previous_results.get('Soil Agent', {}) if previous_results else {}
        
        moisture = observation.get('soil_moisture', 63.0)
        rainfall = observation.get('rainfall', 10.0)
        irrigation_method = farm.get('irrigation_method', 'Drip')
        crop_name = crop.get('name', 'Wheat')

        prompt = (
            f"Crop: {crop_name}\n"
            f"Irrigation Method: {irrigation_method}\n"
            f"Soil moisture: {moisture}%, Rainfall: {rainfall}mm.\n"
            f"Weather Agent Output: {weather_out}\n"
            f"Soil Agent Output: {soil_out}\n\n"
            "Analyze and output standard JSON with the exact fields:\n"
            "{\n"
            "  \"agent\": \"Irrigation Agent\",\n"
            "  \"summary\": \"Watering strategy summary...\",\n"
            "  \"risk_level\": \"Low/Medium/High\",\n"
            "  \"confidence\": integer (0-100),\n"
            "  \"recommendation\": \"Main recommendation...\",\n"
            "  \"actions\": [\n"
            "    {\"title\": \"Task Title\", \"description\": \"Detailed description\", \"priority\": \"High/Medium/Low\"}\n"
            "  ],\n"
            "  \"reasoning\": \"Hydro-engineering reasoning...\"\n"
            "}"
        )

        fallback = {
            "agent": "Irrigation Agent",
            "summary": f"Soil moisture is adequate ({moisture}%) and rainfall was {rainfall}mm. No major watering required immediately.",
            "risk_level": "Low",
            "confidence": 94,
            "recommendation": f"Suspend active drip cycles for the next 24 hours.",
            "actions": [
                {
                    "title": "Check drip system pressure",
                    "description": "Ensure there is no leakage in pipes during the resting interval.",
                    "priority": "Low"
                }
            ],
            "reasoning": f"Current moisture level ({moisture}%) exceeds the trigger threshold (45%) for {crop_name} in vegetative phase. Rainfall adds moisture."
        }

        return GeminiService.generate_json(
            prompt=prompt,
            system_instruction=system_instruction,
            fallback_mock=fallback
        )
