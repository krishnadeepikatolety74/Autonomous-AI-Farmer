from .base_agent import BaseAgent
from services.gemini_service import GeminiService

class FertilizerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Fertilizer Agent",
            description="Generates crop-specific nutrient application plans."
        )

    def run(self, farm, crop, observation, previous_results=None, memory_context=None):
        system_instruction = (
            "You are an expert Crop Nutrition and Fertilizer Advisor AI. "
            "Diagnose fertilizer-related problems from soil and crop data, consider weather before recommending application, "
            "and provide clear, practical advice structured as: Problem → Cause → Solution → Precaution. "
            "Always respond in strict JSON format only — no markdown, no extra text."
        )

        # Collect all available data
        soil_type   = farm.get('soil_type', 'Loam')
        location    = farm.get('location', 'India')

        crop_name   = crop.get('name', 'Unknown')
        crop_stage  = crop.get('stage', 'Vegetative')
        crop_variety = crop.get('variety', '')

        nitrogen    = observation.get('nitrogen', 45.0)
        phosphorus  = observation.get('phosphorus', 30.0)
        potassium   = observation.get('potassium', 120.0)
        ph          = observation.get('soil_ph', 6.5)
        moisture    = observation.get('soil_moisture', 60.0)
        temperature = observation.get('temperature', 28.0)
        humidity    = observation.get('humidity', 65.0)
        rainfall    = observation.get('rainfall', 5.0)
        disease_notes = observation.get('disease_notes', '')

        # Use soil agent output if available
        soil_out = previous_results.get('Soil Agent', {}) if previous_results else {}
        soil_summary = soil_out.get('summary', '')

        prompt = f"""
You are a Fertilizer Advisor AI analyzing crop nutrition needs and recommending fertilizer actions.

=== FARM & CROP INFO ===
Location: {location}
Soil Type: {soil_type}
Crop: {crop_name} {('(' + crop_variety + ')') if crop_variety else ''}
Growth Stage: {crop_stage}
Disease / Stress Notes: {disease_notes if disease_notes else 'None'}

=== SOIL NUTRIENT DATA ===
Nitrogen (N): {nitrogen} kg/ha
Phosphorus (P): {phosphorus} kg/ha
Potassium (K): {potassium} kg/ha
Soil pH: {ph}
Soil Moisture: {moisture}%

=== WEATHER CONDITIONS ===
Temperature: {temperature}°C
Humidity: {humidity}%
Recent Rainfall: {rainfall} mm
{f"Soil Agent Summary: {soil_summary}" if soil_summary else ""}

=== YOUR TASK ===
1. Identify the top fertilizer-related problem(s) for this crop and soil.
2. For each problem explain: what is wrong, why it may be happening, what to do, and what to avoid.
3. Check whether weather is favorable for fertilizer application:
   - If rainfall > 20mm recently or rain is expected: warn about nutrient runoff/leaching.
   - If temperature > 38°C: warn about ammonia volatilization for urea.
   - If conditions are favorable: confirm the application window is suitable.
4. Recommend specific fertilizer types from this list if applicable:
   Urea, DAP, MOP/Potash, SSP, NPK 10:26:26, NPK 19:19:19, Ammonium Sulphate.
   Only recommend what is needed — do not suggest all of them.
5. Provide dose (kg/ha) and timing guidance for each recommendation.

Return ONLY this exact JSON (no markdown, no text outside JSON):
{{
  "agent": "Fertilizer Agent",
  "summary": "2-3 sentence summary of the main fertilizer situation",
  "risk_level": "Low / Medium / High",
  "confidence": <integer 0-100>,
  "problems": [
    {{
      "problem": "What is wrong (e.g. Nitrogen deficiency suspected)",
      "possible_cause": "Why this is happening",
      "solution": "What the farmer should do — specific fertilizer, dose, timing",
      "precaution": "What to avoid or watch out for"
    }}
  ],
  "weather_window": {{
    "favorable": true or false,
    "reason": "Explanation of whether conditions are good for fertilizer application"
  }},
  "recommended_fertilizers": [
    {{
      "name": "Fertilizer name",
      "dose_kg_per_ha": <number>,
      "timing": "When and how to apply",
      "purpose": "What nutrient it addresses"
    }}
  ],
  "recommendation": "Overall main recommendation for the farmer",
  "actions": [
    {{"title": "Action title", "description": "Detailed what to do", "priority": "High / Medium / Low"}}
  ],
  "reasoning": "Brief explanation of how you arrived at these conclusions"
}}
"""

        # Dynamic fallback based on real data
        high_rainfall = rainfall > 20
        hot = temperature > 38
        n_deficient = nitrogen < 50
        p_deficient = phosphorus < 25
        k_deficient = potassium < 80

        problems = []
        if n_deficient:
            problems.append({
                "problem": f"Nitrogen deficiency suspected — current level {nitrogen} kg/ha is below the recommended 55–65 kg/ha for {crop_name} at {crop_stage} stage.",
                "possible_cause": "Insufficient nitrogen application, leaching from recent rainfall, or high crop demand during active growth.",
                "solution": f"Apply Urea at 25–30 kg/ha after rainfall subsides. Incorporate lightly into soil for best uptake." if not high_rainfall else f"Wait for rainfall to stop before applying Urea. Pre-apply SSP to maintain phosphorus and prevent further leaching.",
                "precaution": "Do not apply urea during heavy rain — it will leach away. Avoid over-application which causes ammonia burn."
            })
        if p_deficient:
            problems.append({
                "problem": f"Phosphorus is low at {phosphorus} kg/ha — may limit root development and flowering.",
                "possible_cause": "Soil pH may be locking up phosphorus, or insufficient basal P application at sowing.",
                "solution": "Apply DAP at 50 kg/ha as a basal dose, or SSP at 100 kg/ha if soil pH is above 7.0.",
                "precaution": "Avoid applying phosphorus with high-calcium lime simultaneously as this can further lock up P."
            })
        if k_deficient:
            problems.append({
                "problem": f"Potassium is low at {potassium} kg/ha — may cause leaf edge browning and reduced stress tolerance.",
                "possible_cause": "Sandy soils leach potassium easily. Heavy fruiting or grain-fill stages increase K demand significantly.",
                "solution": "Apply MOP (Muriate of Potash) at 30–40 kg/ha split between top-dressing doses.",
                "precaution": "Do not apply K in excess — it can interfere with magnesium uptake."
            })
        if not problems:
            problems.append({
                "problem": "No major nutrient deficiency detected based on current data.",
                "possible_cause": "Nutrient levels appear within acceptable ranges for current crop stage.",
                "solution": "Continue monitoring and conduct a soil test at the next crop stage transition.",
                "precaution": "Do not apply unnecessary fertilizer — over-fertilization increases cost and environmental risk."
            })

        fallback = {
            "agent": "Fertilizer Agent",
            "summary": f"Analyzing fertilizer needs for {crop_name} at {crop_stage} stage on {soil_type} soil. {'Nitrogen deficiency is the primary concern.' if n_deficient else 'Nutrient levels are broadly acceptable.'}",
            "risk_level": "High" if n_deficient else ("Medium" if p_deficient or k_deficient else "Low"),
            "confidence": 78,
            "problems": problems,
            "weather_window": {
                "favorable": not high_rainfall and not hot,
                "reason": (
                    f"Recent rainfall of {rainfall}mm creates high runoff risk — delay fertilizer application by 2–3 days." if high_rainfall else
                    f"Temperature of {temperature}°C risks ammonia volatilization from urea — apply in early morning or evening." if hot else
                    "Weather conditions appear favorable for fertilizer application."
                )
            },
            "recommended_fertilizers": [
                {"name": "Urea", "dose_kg_per_ha": 25, "timing": "Top-dress after rainfall, early morning", "purpose": "Nitrogen supplement"}
            ] if n_deficient else [],
            "recommendation": f"{'Prioritize nitrogen replenishment for ' + crop_name + ' before the next growth phase.' if n_deficient else 'Maintain current nutrient management. Conduct soil test at next stage.'}",
            "actions": [
                {
                    "title": f"{'Apply Urea — Nitrogen Deficiency' if n_deficient else 'Monitor Soil Nutrients'}",
                    "description": f"{'Apply 25 kg/ha Urea after rain subsides. Incorporate lightly into top 5cm of soil.' if n_deficient else 'Run a soil test at the next crop stage transition to confirm nutrient adequacy.'}",
                    "priority": "High" if n_deficient else "Low"
                }
            ],
            "reasoning": f"N={nitrogen}, P={phosphorus}, K={potassium} kg/ha on {soil_type} soil with pH {ph}. {'High rainfall of ' + str(rainfall) + 'mm warrants delaying application.' if high_rainfall else 'Weather is currently suitable for application.'}"
        }

        return GeminiService.generate_json(
            prompt=prompt,
            system_instruction=system_instruction,
            fallback_mock=fallback
        )
