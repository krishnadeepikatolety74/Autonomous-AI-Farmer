from .base_agent import BaseAgent
from services.gemini_service import GeminiService

class DiseaseAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Crop Disease Agent",
            description="Scans crop health indices and logs alerts regarding potential pathogen outbreaks."
        )

    def run(self, farm, crop, observation, previous_results=None, memory_context=None):
        system_instruction = (
            "You are an expert Phytopathologist Crop Disease AI Agent. Evaluate field observations "
            "and suggest disease mitigation guidelines in strict JSON format."
        )
        
        health_index = observation.get('crop_health', 82.0)
        disease_notes = observation.get('disease_notes', 'None')
        crop_name = crop.get('name', 'Wheat')
        stage = crop.get('stage', 'Vegetative')

        prompt = (
            f"Crop: {crop_name} (Stage: {stage})\n"
            f"Crop Health Index: {health_index}%.\n"
            f"Farmer Observations: {disease_notes}\n\n"
            "Analyze and output standard JSON with the exact fields:\n"
            "{\n"
            "  \"agent\": \"Crop Disease Agent\",\n"
            "  \"summary\": \"Crop disease detection summary...\",\n"
            "  \"risk_level\": \"Low/Medium/High\",\n"
            "  \"confidence\": integer (0-100),\n"
            "  \"recommendation\": \"Main recommendation...\",\n"
            "  \"actions\": [\n"
            "    {\"title\": \"Task Title\", \"description\": \"Detailed description\", \"priority\": \"High/Medium/Low\"}\n"
            "  ],\n"
            "  \"reasoning\": \"Phytopathology analysis reasoning...\"\n"
            "}"
        )

        fallback = {
            "agent": "Crop Disease Agent",
            "summary": f"Crop health index is strong at {health_index}%. No immediate fungal or insect attacks detected.",
            "risk_level": "Low" if "yellow" not in disease_notes.lower() else "Medium",
            "confidence": 95,
            "recommendation": "Maintain protective neem oil sprays as a preemptive measure.",
            "actions": [
                {
                    "title": "Perform routine weed sweep",
                    "description": "Remove weeds around borders to minimize pests and potential vectors.",
                    "priority": "Low"
                }
            ],
            "reasoning": f"Health index {health_index}% reflects optimal leaf chlorophyll levels. Current notes ({disease_notes}) do not present active warning markers."
        }

        return GeminiService.generate_json(
            prompt=prompt,
            system_instruction=system_instruction,
            fallback_mock=fallback
        )
