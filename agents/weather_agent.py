from .base_agent import BaseAgent
from services.gemini_service import GeminiService
from services.weather_service import WeatherService

class WeatherAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Weather Agent",
            description="Monitors meteorological inputs and evaluates crop-climate hazards."
        )

    def run(self, farm, crop, observation, previous_results=None, memory_context=None):
        system_instruction = (
            "You are an expert Agricultural Weather AI Agent. Analyze weather metrics and "
            "provide dynamic crop-impact advisories in strict JSON format."
        )

        # ── Stored telemetry (manual entries from observation form) ──────────
        obs_temp      = observation.get('temperature',  24.0)
        obs_humidity  = observation.get('humidity',     68.0)
        obs_rainfall  = observation.get('rainfall',     10.0)
        crop_name     = crop.get('name',  'Wheat')
        stage         = crop.get('stage', 'Vegetative')
        location      = farm.get('location', 'India')

        # ── Live weather fetch from Open-Meteo ────────────────────────────────
        live = WeatherService.fetch_live_weather(location)
        live_weather_available = live is not None

        # When live data is available, use it as the primary source
        if live_weather_available:
            temperature = live['temperature_c']
            humidity    = live['humidity_pct']
            rainfall    = live['precipitation_mm']
        else:
            temperature = obs_temp
            humidity    = obs_humidity
            rainfall    = obs_rainfall

        # ── Build context string for Gemini ──────────────────────────────────
        weather_section = ""
        if live_weather_available:
            weather_section = (
                f"\n=== LIVE WEATHER DATA (fetched at analysis time) ===\n"
                f"Resolved Location  : {live['location']}\n"
                f"Condition          : {live['condition']}\n"
                f"Temperature        : {live['temperature_c']}°C  (feels like {live['feels_like_c']}°C)\n"
                f"Humidity           : {live['humidity_pct']}%\n"
                f"Precipitation      : {live['precipitation_mm']} mm (last hour)\n"
                f"Wind Speed         : {live['wind_speed_kmh']} km/h at {live['wind_direction']}°\n"
                f"UV Index           : {live['uv_index']}\n"
                f"Time of Day        : {'Daytime' if live['is_day'] else 'Night-time'}\n"
                f"(These figures come from live Open-Meteo API data, NOT from stored sensor observations.)\n"
            )
        else:
            weather_section = (
                f"\n=== WEATHER DATA (from stored farm observations — live fetch unavailable) ===\n"
                f"Temperature : {temperature}°C\n"
                f"Humidity    : {humidity}%\n"
                f"Rainfall    : {rainfall} mm\n"
            )

        sensor_section = (
            f"\n=== FARM SENSOR OBSERVATIONS (manual entry) ===\n"
            f"Soil Moisture : {observation.get('soil_moisture', 0)}%\n"
            f"Soil pH       : {observation.get('soil_ph', 7.0)}\n"
            f"Crop Health   : {observation.get('crop_health', 0)}%\n"
            f"Disease Notes : {observation.get('disease_notes') or 'None'}\n"
            f"Market Price  : {observation.get('market_price', 0.0)} INR/quintal\n"
        )

        prompt = (
            f"Farm Location : {location}\n"
            f"Crop          : {crop_name} (Stage: {stage})\n"
            f"{weather_section}"
            f"{sensor_section}"
            "\nAnalyze the weather impact on the crop and output standard JSON with the exact fields:\n"
            "{\n"
            "  \"agent\": \"Weather Agent\",\n"
            "  \"summary\": \"Weather assessment summary...\",\n"
            "  \"risk_level\": \"Low/Medium/High\",\n"
            "  \"confidence\": integer (0-100),\n"
            "  \"recommendation\": \"Main recommendation...\",\n"
            "  \"actions\": [\n"
            "    {\"title\": \"Task Title\", \"description\": \"Detailed description\", \"priority\": \"High/Medium/Low\"}\n"
            "  ],\n"
            "  \"reasoning\": \"Agronomic reasoning...\"\n"
            "}"
        )

        fallback = {
            "agent":          "Weather Agent",
            "summary":        f"{'Live' if live_weather_available else 'Stored'} weather data: {temperature}°C, {humidity}% humidity, {rainfall}mm rainfall for {crop_name} at {location}.",
            "risk_level":     "Low" if rainfall > 5 else "Medium",
            "confidence":     88 if live_weather_available else 75,
            "recommendation": "Monitor conditions and maintain standard field scheduling.",
            "actions": [
                {
                    "title":       "Monitor wind gusts" if not live_weather_available else f"Monitor {live.get('condition', 'conditions')}",
                    "description": "Keep an eye on weather updates as crop is in active growth phase.",
                    "priority":    "Low"
                }
            ],
            "reasoning": (
                f"{'Live' if live_weather_available else 'Stored'} data shows {temperature}°C temperature and "
                f"{humidity}% humidity. Rainfall of {rainfall}mm {'per hour' if live_weather_available else ''}. "
                f"{'UV Index: ' + str(live.get('uv_index', 0)) + '. ' if live_weather_available else ''}"
                f"Conditions are within manageable range for {crop_name}."
            ),
            "live_weather_fetched": live_weather_available,
            "live_weather":         live or {},
        }

        result = GeminiService.generate_json(
            prompt=prompt,
            system_instruction=system_instruction,
            fallback_mock=fallback
        )

        # Attach live weather data to result for frontend display
        if isinstance(result, dict):
            result['live_weather_fetched'] = live_weather_available
            result['live_weather']         = live or {}

        return result

