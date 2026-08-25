from .base_agent import BaseAgent
from services.gemini_service import GeminiService

class MarketAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Market Agent",
            description="Tracks commodity prices and optimal selling windows."
        )

    def run(self, farm, crop, observation, previous_results=None, memory_context=None):
        system_instruction = (
            "You are an expert Agricultural Market Intelligence AI for Indian farmers. "
            "Answer questions about vegetables, fruits, flowers, grains, pulses, and other agricultural produce. "
            "Provide market trends, price analysis, demand-supply context, and selling recommendations. "
            "CRITICAL: Never fabricate exact current live prices — label any price you state clearly as 'Estimated' "
            "or 'Historical Reference' unless you have real-time data. "
            "Always respond in strict JSON format only — no markdown, no extra text."
        )

        crop_name     = crop.get('name', 'Unknown')
        crop_stage    = crop.get('stage', 'Vegetative')
        location      = farm.get('location', 'India')
        farm_area     = farm.get('area', 0)
        soil_type     = farm.get('soil_type', 'Loam')
        market_price  = observation.get('market_price', 0)
        temperature   = observation.get('temperature', 28.0)
        humidity      = observation.get('humidity', 65.0)
        rainfall      = observation.get('rainfall', 5.0)
        crop_health   = observation.get('crop_health', 80.0)
        disease_notes = observation.get('disease_notes', '')

        # Reference price from farmer's own last record (not live API)
        price_label = "Farmer-Recorded Price" if market_price > 0 else "Not recorded"
        price_note = f"The farmer last recorded: ₹{market_price}/quintal ({price_label})." if market_price > 0 else "No market price has been recorded by the farmer."

        prompt = f"""
You are an Agricultural Market Intelligence AI helping an Indian farmer make smart selling decisions.

=== FARM & CROP INFO ===
Location: {location}
Farm Area: {farm_area} acres
Crop: {crop_name}
Growth Stage: {crop_stage}
Crop Health Index: {crop_health}%
Disease / Stress Notes: {disease_notes if disease_notes else 'None'}

=== PRICE DATA ===
{price_note}
NOTE: This is the farmer's own recorded reference price, NOT a live mandi price feed.
Do NOT present this as today's market price. Clearly label it as the farmer's reference.

=== WEATHER CONDITIONS ===
Temperature: {temperature}°C
Humidity: {humidity}%
Recent Rainfall: {rainfall} mm

=== YOUR TASK ===
1. Provide market context for {crop_name} in the {location} region:
   - General price trend (seasonal, demand-supply context)
   - Whether current timing is favorable for selling
   - Storage vs sell-now analysis based on crop stage and health

2. Price analysis:
   - If the farmer's reference price is available, comment on whether it appears low, fair, or above market expectations (as an estimate — do not claim it is live data).
   - Explain what factors affect this crop's price (season, demand, surplus/deficit areas, weather impact on supply).

3. Price increase scenario:
   - If the farmer considers increasing their price by 10–15%, analyze likely buyer response, demand impact, and revenue implication.

4. Price decrease scenario:
   - If the farmer considers reducing price by 10–15%, analyze likely sales speed impact, revenue effect, and risk.

5. Weather impact on market:
   - Explain how current weather ({temperature}°C, {rainfall}mm rain) affects produce quality, transportation, and market price.

6. Actionable recommendation:
   - Should the farmer sell now or wait?
   - Is there a better market/channel suggestion?

Return ONLY this exact JSON (no markdown, no text outside JSON):
{{
  "agent": "Market Agent",
  "summary": "2-3 sentence market intelligence summary for {crop_name}",
  "risk_level": "Low / Medium / High",
  "confidence": <integer 0-100>,
  "price_data": {{
    "farmer_reference": {market_price if market_price > 0 else 'null'},
    "label": "Farmer-Recorded / Estimated / Not available",
    "data_note": "Explanation of what the price represents — NOT live data"
  }},
  "market_trend": {{
    "direction": "Rising / Stable / Falling / Seasonal",
    "reason": "Why prices are moving in this direction"
  }},
  "price_increase_analysis": {{
    "scenario": "10-15% price increase",
    "likely_buyer_response": "What buyers would likely do",
    "revenue_impact": "Higher/Lower/Uncertain and why",
    "risk": "Key risk of raising price",
    "recommendation": "Advice on this scenario"
  }},
  "price_decrease_analysis": {{
    "scenario": "10-15% price decrease",
    "sales_speed_impact": "How much faster it may sell",
    "revenue_impact": "How margin/total revenue is affected",
    "risk": "Key risk of reducing price",
    "recommendation": "Advice on this scenario"
  }},
  "weather_market_impact": "How current weather affects quality, logistics, and price",
  "sell_or_wait": "Sell Now / Wait / Partial Sale — with reasoning",
  "recommendation": "Main actionable recommendation for the farmer",
  "actions": [
    {{"title": "Action title", "description": "Detailed what to do", "priority": "High / Medium / Low"}}
  ],
  "reasoning": "Brief explanation of your market analysis logic"
}}
"""

        # Intelligent fallback based on crop stage
        near_harvest = crop_stage in ['Maturity', 'Pod Fill']
        high_moisture_risk = humidity > 80 or rainfall > 30

        fallback = {
            "agent": "Market Agent",
            "summary": (
                f"{crop_name} is at {crop_stage} stage. "
                f"{'Harvest is approaching — evaluate storage vs. immediate sale carefully.' if near_harvest else 'Crop is not yet at harvest stage — focus on growth management before market decisions.'} "
                f"Market conditions in {location} are subject to seasonal supply-demand dynamics."
            ),
            "risk_level": "Medium",
            "confidence": 65,
            "price_data": {
                "farmer_reference": market_price if market_price > 0 else None,
                "label": "Farmer-Recorded" if market_price > 0 else "Not available",
                "data_note": "This is the farmer's own recorded reference price, not a live mandi feed. Actual market prices may vary."
            },
            "market_trend": {
                "direction": "Seasonal",
                "reason": f"Price trends for {crop_name} are highly seasonal. Post-harvest periods typically see lower prices due to surplus supply. Off-season production can command premium prices."
            },
            "price_increase_analysis": {
                "scenario": "10-15% price increase",
                "likely_buyer_response": "Buyers may shift to alternative suppliers or commodities if the price increase is significantly above the prevailing mandi rate.",
                "revenue_impact": "Higher revenue per unit if buyers accept the price; potential drop in volume sold if they do not.",
                "risk": "Losing buyers to competitors offering lower prices. Risk is higher in a surplus season.",
                "recommendation": "Test a small quantity at the higher price first. Maintain quality standards to justify the premium."
            },
            "price_decrease_analysis": {
                "scenario": "10-15% price decrease",
                "sales_speed_impact": "A lower price typically increases buyer interest and sales velocity, especially in competitive markets.",
                "revenue_impact": "Lower margin per unit. Unless volume increase compensates, total revenue may decline.",
                "risk": "Difficulty reverting to higher prices once buyers anchor to the lower rate.",
                "recommendation": "Reduce price only if the crop is at risk of quality loss from storage, or if cash flow urgently requires quick sale."
            },
            "weather_market_impact": (
                f"High humidity ({humidity}%) and recent rainfall ({rainfall}mm) increase the risk of post-harvest quality loss. "
                "Buyers may reduce offers for damp or partially spoiled produce. Ensure proper drying and storage before sale." 
                if high_moisture_risk else
                f"Weather conditions ({temperature}°C, {humidity}% humidity) are relatively stable. Produce quality should be maintainable with standard storage."
            ),
            "sell_or_wait": (
                f"Partial Sale — Sell enough to cover immediate costs and store the remainder if storage conditions allow. "
                f"Quality risk from {humidity}% humidity warrants selling sooner rather than later."
                if high_moisture_risk and near_harvest else
                f"Wait — {crop_name} is at {crop_stage} stage and not yet ready for optimal sale." if not near_harvest else
                "Sell Now — Crop is at maturity. Delaying sale increases storage cost and quality risk."
            ),
            "recommendation": (
                f"{'Begin preparing for sale — crop is near harvest. Assess quality, arrange transport, and contact buyers in advance.' if near_harvest else 'Focus on crop management now. Begin market research at least 2-3 weeks before expected harvest.'}"
            ),
            "actions": [
                {
                    "title": "Research local mandi prices",
                    "description": f"Check the Agmarknet portal or local mandi for current {crop_name} prices in {location} before deciding on a selling price.",
                    "priority": "High" if near_harvest else "Medium"
                },
                {
                    "title": "Assess post-harvest storage quality",
                    "description": "Ensure grain moisture is below 12-14% and produce is properly sorted. Poor quality reduces buyer offers significantly.",
                    "priority": "High" if high_moisture_risk else "Low"
                }
            ],
            "reasoning": (
                f"Analysis based on crop stage ({crop_stage}), weather conditions ({temperature}°C, {rainfall}mm), "
                f"and farmer reference price ({'₹' + str(market_price) + '/q' if market_price > 0 else 'not provided'}). "
                "No live mandi data is connected — recommendations are based on agricultural market principles and seasonal patterns."
            )
        }

        return GeminiService.generate_json(
            prompt=prompt,
            system_instruction=system_instruction,
            fallback_mock=fallback
        )
