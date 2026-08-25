from .base_agent import BaseAgent
from services.gemini_service import GeminiService

class SoilAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Soil Agent",
            description="Analyzes soil health, hydration, and nutrient (N-P-K) levels."
        )

    def run(self, farm, crop, observation, previous_results=None, memory_context=None):
        system_instruction = (
            "You are an expert Agronomist and Soil Scientist AI. "
            "Analyze the given soil, crop, and weather conditions to provide a comprehensive, "
            "practical soil health assessment and crop suitability report. "
            "Always respond in strict JSON format only — no markdown, no extra text."
        )

        # Collect all available data
        soil_type     = farm.get('soil_type', 'Loam')
        location      = farm.get('location', 'India')
        farm_area     = farm.get('area', 0)

        crop_name     = crop.get('name', 'Unknown')
        crop_variety  = crop.get('variety', '')
        crop_stage    = crop.get('stage', 'Vegetative')

        moisture      = observation.get('soil_moisture', 60.0)
        ph            = observation.get('soil_ph', 6.5)
        nitrogen      = observation.get('nitrogen', 45.0)
        phosphorus    = observation.get('phosphorus', 30.0)
        potassium     = observation.get('potassium', 120.0)
        temperature   = observation.get('temperature', 28.0)
        humidity      = observation.get('humidity', 65.0)
        rainfall      = observation.get('rainfall', 5.0)
        crop_health   = observation.get('crop_health', 80.0)
        disease_notes = observation.get('disease_notes', '')

        prompt = f"""
You are analyzing soil and weather data for a farm. Use ALL the information below to produce your assessment.

=== FARM INFO ===
Location: {location}
Farm Area: {farm_area} acres
Soil Type: {soil_type}

=== CROP INFO ===
Crop: {crop_name} {('(' + crop_variety + ')') if crop_variety else ''}
Growth Stage: {crop_stage}
Crop Health Index: {crop_health}%
Field Notes: {disease_notes if disease_notes else 'None reported'}

=== SOIL MEASUREMENTS ===
Soil Moisture: {moisture}%
Soil pH: {ph}
Nitrogen (N): {nitrogen} kg/ha
Phosphorus (P): {phosphorus} kg/ha
Potassium (K): {potassium} kg/ha

=== WEATHER / ENVIRONMENT ===
Temperature: {temperature}°C
Humidity: {humidity}%
Rainfall (recent): {rainfall} mm

=== YOUR TASK ===
1. Assess overall soil health (Good / Moderate / Poor) with a clear explanation.
2. Analyze:
   - Soil fertility rating
   - Soil pH suitability for the current crop
   - Moisture condition (too dry / optimal / waterlogged)
   - Nutrient availability (N, P, K — adequate / deficient / excess)
   - Possible nutrient deficiencies or toxicities
   - Soil risks (salinity, compaction, leaching, erosion, etc.)

3. Determine crop suitability:
   - List crops highly suitable, suitable, and marginally suitable for these soil conditions.
   - Provide 2-3 recommended intercropping or mixed-crop combinations.
   - Explain briefly why each grouping works.

4. Weather-soil interaction:
   - Comment on how current temperature, humidity, and rainfall affect soil nutrient availability and crop growth.
   - If heavy rain is present/forecast, warn about nutrient leaching risk.
   - If dry, advise on irrigation and moisture retention.

5. Fertilizer conditions:
   - Based on soil nutrients and weather, identify the most urgent fertilizer need.
   - If rain is expected soon, advise on timing to prevent runoff loss.

Return ONLY this exact JSON (no markdown, no explanation outside JSON):
{{
  "agent": "Soil Agent",
  "summary": "Brief soil health summary in 2-3 sentences",
  "soil_health": "Good / Moderate / Poor",
  "risk_level": "Low / Medium / High",
  "confidence": <integer 0-100>,
  "ph_status": "Suitable / Too Acidic / Too Alkaline",
  "moisture_status": "Optimal / Too Dry / Waterlogged",
  "nutrient_summary": {{
    "nitrogen": "Adequate / Deficient / Excess",
    "phosphorus": "Adequate / Deficient / Excess",
    "potassium": "Adequate / Deficient / Excess"
  }},
  "crop_suitability": {{
    "highly_suitable": ["Crop1", "Crop2"],
    "suitable": ["Crop3", "Crop4"],
    "marginally_suitable": ["Crop5"],
    "intercropping": ["Crop1 + Crop3", "Crop2 + Crop4"]
  }},
  "weather_soil_interaction": "Explanation of how weather affects soil and crops right now",
  "fertilizer_urgency": "What fertilizer action is most urgent and why",
  "recommendation": "Main overall recommendation for this farmer",
  "actions": [
    {{"title": "Action title", "description": "Detailed description of what to do", "priority": "High / Medium / Low"}}
  ],
  "reasoning": "Brief explanation of key findings and analysis logic"
}}
"""

        fallback = {
            "agent": "Soil Agent",
            "summary": f"{soil_type} soil with pH {ph}. Moisture at {moisture}% for {crop_name} at {crop_stage} stage. Nutrient levels require review.",
            "soil_health": "Moderate" if (50 <= moisture <= 80 and 5.5 <= ph <= 7.5) else "Poor",
            "risk_level": "Medium",
            "confidence": 72,
            "ph_status": "Suitable" if 5.5 <= ph <= 7.5 else ("Too Acidic" if ph < 5.5 else "Too Alkaline"),
            "moisture_status": "Optimal" if 40 <= moisture <= 80 else ("Too Dry" if moisture < 40 else "Waterlogged"),
            "nutrient_summary": {
                "nitrogen": "Deficient" if nitrogen < 50 else "Adequate",
                "phosphorus": "Adequate" if 20 <= phosphorus <= 60 else "Deficient",
                "potassium": "Adequate" if potassium >= 80 else "Deficient"
            },
            "crop_suitability": {
                "highly_suitable": [crop_name],
                "suitable": ["Maize", "Sorghum"],
                "marginally_suitable": ["Barley"],
                "intercropping": [f"{crop_name} + Legume", "Maize + Beans"]
            },
            "weather_soil_interaction": (
                f"At {temperature}°C with {humidity}% humidity and recent rainfall of {rainfall}mm, "
                "soil nutrient uptake conditions are moderate. Monitor for nutrient leaching if rainfall continues."
                if rainfall > 20 else
                f"At {temperature}°C with {humidity}% humidity, soil moisture of {moisture}% is in range. "
                "Ensure consistent irrigation if rainfall remains low."
            ),
            "fertilizer_urgency": (
                f"Nitrogen is below optimum at {nitrogen} kg/ha. Apply 25-30 kg/ha urea when rain subsides."
                if nitrogen < 50 else
                "Nutrient levels are broadly adequate. Monitor potassium if crop shows leaf edge browning."
            ),
            "recommendation": f"Maintain soil moisture between 50-70% for {crop_name}. Address nitrogen levels before next growth phase.",
            "actions": [
                {
                    "title": "Monitor and address nitrogen deficit",
                    "description": f"Nitrogen at {nitrogen} kg/ha is below the optimal 55-65 kg/ha for {crop_name}. Apply urea or organic nitrogen source at next available dry window.",
                    "priority": "High" if nitrogen < 45 else "Medium"
                }
            ],
            "reasoning": f"pH {ph} is {'suitable' if 5.5 <= ph <= 7.5 else 'outside optimal range'} for {crop_name}. Nitrogen level is the primary constraint. Weather conditions show {rainfall}mm recent rainfall — monitor leaching risk."
        }

        return GeminiService.generate_json(
            prompt=prompt,
            system_instruction=system_instruction,
            fallback_mock=fallback
        )
