from .base_agent import BaseAgent
from services.gemini_service import GeminiService

class FarmPlanningAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Farm Planning Agent",
            description="Coordinates specialized agent streams and synthesizes a unified crop strategy."
        )

    def run(self, farm, crop, observation, previous_results=None, memory_context=None):
        system_instruction = (
            "You are the Farm Planning Agent (Coordinator). Your role is to receive findings "
            "from all specialized sub-agents, resolve conflicts, and synthesize a single comprehensive "
            "farm operations action plan in strict JSON format."
        )
        
        crop_name = crop.get('name', 'Wheat')
        location = farm.get('location', 'Punjab, India')

        prompt = (
            f"Farm Location: {location}\n"
            f"Crop: {crop_name}\n"
            f"Specialized Agent Outputs: {previous_results}\n"
            f"Historical Memory Context: {memory_context}\n\n"
            "Analyze and output standard JSON with the exact fields:\n"
            "{\n"
            "  \"agent\": \"Farm Planning Agent\",\n"
            "  \"overall_status\": \"Good/Fair/Critical\",\n"
            "  \"overall_risk\": \"Low/Medium/High\",\n"
            "  \"summary\": \"SaaS dashboard plan overview...\",\n"
            "  \"priority_actions\": [\n"
            "    {\"agent\": \"Agent Name\", \"title\": \"Task Title\", \"description\": \"Detailed description\", \"priority\": \"High/Medium/Low\"}\n"
            "  ],\n"
            "  \"final_plan\": \"Comprehensive farm operational plan paragraph...\",\n"
            "  \"confidence\": integer (0-100)\n"
            "}"
        )

        fallback = {
            "agent": "Farm Planning Agent",
            "overall_status": "Good",
            "overall_risk": "Low",
            "summary": "The farm is in healthy status. Main priority is mild nitrogen correction.",
            "priority_actions": [
                {
                    "agent": "Fertilizer Agent",
                    "title": "Apply Nitrogen dressing",
                    "description": "Scatter Urea early in the morning.",
                    "priority": "High"
                }
            ],
            "final_plan": f"Plan for {crop_name} in {location} is running smoothly. General irrigation is suspended temporarily.",
            "confidence": 93
        }

        return GeminiService.generate_json(
            prompt=prompt,
            system_instruction=system_instruction,
            fallback_mock=fallback
        )
