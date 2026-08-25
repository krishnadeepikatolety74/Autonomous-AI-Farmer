"""
WeatherService — fetches live weather from Open-Meteo (free, no API key required).

Flow:
  1. Geocode the farm location string -> lat/lon using Open-Meteo Geocoding API
     • Fetches top-5 results, scores them by name/admin1 match with the input
     • Falls back to state capital when input is a known Indian state name
  2. Fetch current weather metrics from Open-Meteo Weather API
  3. Return a structured dict with temperature, humidity, precipitation, wind,
     UV index, and a human-readable weather description.

Graceful fallback: if geocoding fails or the API is unreachable, returns None
so the Weather Agent falls back to the stored observation telemetry.
"""

import requests
import time
import threading

# WMO Weather Code -> human-readable description
WMO_CODE_DESCRIPTIONS = {
    0:  "Clear sky",
    1:  "Mainly clear",
    2:  "Partly cloudy",
    3:  "Overcast",
    45: "Foggy",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}

# Indian state → (capital city, state display name)
# When a user enters only a state name, we geocode the capital for accurate coords
INDIAN_STATE_CAPITALS = {
    "andhra pradesh":          ("Vijayawada",          "Andhra Pradesh, India"),
    "arunachal pradesh":       ("Itanagar",            "Arunachal Pradesh, India"),
    "assam":                   ("Dispur",              "Assam, India"),
    "bihar":                   ("Patna",               "Bihar, India"),
    "chhattisgarh":            ("Raipur",              "Chhattisgarh, India"),
    "goa":                     ("Panaji",              "Goa, India"),
    "gujarat":                 ("Gandhinagar",         "Gujarat, India"),
    "haryana":                 ("Chandigarh",          "Haryana, India"),
    "himachal pradesh":        ("Shimla",              "Himachal Pradesh, India"),
    "jharkhand":               ("Ranchi",              "Jharkhand, India"),
    "karnataka":               ("Bangalore",           "Karnataka, India"),
    "kerala":                  ("Thiruvananthapuram",  "Kerala, India"),
    "madhya pradesh":          ("Bhopal",              "Madhya Pradesh, India"),
    "maharashtra":             ("Mumbai",              "Maharashtra, India"),
    "manipur":                 ("Imphal",             "Manipur, India"),
    "meghalaya":               ("Shillong",            "Meghalaya, India"),
    "mizoram":                 ("Aizawl",              "Mizoram, India"),
    "nagaland":                ("Kohima",              "Nagaland, India"),
    "odisha":                  ("Bhubaneswar",         "Odisha, India"),
    "punjab":                  ("Chandigarh",          "Punjab, India"),
    "rajasthan":               ("Jaipur",              "Rajasthan, India"),
    "sikkim":                  ("Gangtok",             "Sikkim, India"),
    "tamil nadu":              ("Chennai",             "Tamil Nadu, India"),
    "telangana":               ("Hyderabad",           "Telangana, India"),
    "tripura":                 ("Agartala",            "Tripura, India"),
    "uttar pradesh":           ("Lucknow",             "Uttar Pradesh, India"),
    "uttarakhand":             ("Dehradun",            "Uttarakhand, India"),
    "west bengal":             ("Kolkata",             "West Bengal, India"),
    # Union Territories
    "delhi":                   ("New Delhi",           "Delhi, India"),
    "jammu and kashmir":       ("Srinagar",            "Jammu & Kashmir, India"),
    "ladakh":                  ("Leh",                 "Ladakh, India"),
    "puducherry":              ("Puducherry",          "Puducherry, India"),
    "chandigarh":              ("Chandigarh",          "Chandigarh, India"),
    # Common abbreviations / alternate spellings
    "andhra":                  ("Vijayawada",          "Andhra Pradesh, India"),
    "ap":                      ("Vijayawada",          "Andhra Pradesh, India"),
    "up":                      ("Lucknow",             "Uttar Pradesh, India"),
    "mp":                      ("Bhopal",              "Madhya Pradesh, India"),
    "hp":                      ("Shimla",              "Himachal Pradesh, India"),
    "tn":                      ("Chennai",             "Tamil Nadu, India"),
    "wb":                      ("Kolkata",             "West Bengal, India"),
    "orissa":                  ("Bhubaneswar",         "Odisha, India"),
    "bengal":                  ("Kolkata",             "West Bengal, India"),
    "bangalore":               ("Bangalore",           "Karnataka, India"),
    "bombay":                  ("Mumbai",              "Maharashtra, India"),
    "madras":                  ("Chennai",             "Tamil Nadu, India"),
    "calcutta":                ("Kolkata",             "West Bengal, India"),
}


def _score_result(result: dict, query_tokens: set) -> int:
    """
    Score a geocoding result by how many tokens from the query appear in the
    result's name / admin1 / country fields. Higher = better match.
    """
    score = 0
    for field in ("name", "admin1", "admin2", "country"):
        value = (result.get(field) or "").lower()
        for token in query_tokens:
            if token and token in value:
                score += 1
    return score


class WeatherService:
    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
    WEATHER_URL   = "https://api.open-meteo.com/v1/forecast"
    TIMEOUT       = 8  # seconds

    # Caching structures for performance optimization
    _geocode_cache = {}
    _geocode_cache_lock = threading.Lock()
    _weather_cache = {}
    _weather_cache_lock = threading.Lock()
    WEATHER_CACHE_DURATION = 300  # cache duration in seconds (5 minutes)

    @staticmethod
    def _build_display(result: dict, original_location: str) -> str:
        """Build a clean 'City, State, Country' display string from a geocoding result."""
        parts = []
        name    = (result.get("name") or "").strip()
        admin1  = (result.get("admin1") or "").strip()
        country = (result.get("country") or "").strip()

        if name:
            parts.append(name)
        if admin1 and admin1 != name:
            parts.append(admin1)
        if country and country not in parts:
            parts.append(country)

        return ", ".join(p for p in parts if p) or original_location

    @staticmethod
    def geocode(location: str):
        """
        Convert a free-text location string into lat/lon + display name.

        Strategy:
          1. Check if location matches a known Indian state -> use capital city
          2. Otherwise fetch top 5 Open-Meteo results and pick the best match
             by scoring how many query tokens appear in each result's fields

        Returns:
            {
                'lat': float,
                'lon': float,
                'display': str,   # "City, State, Country"
            }
        or None if not found.
        """
        if not location or not location.strip():
            return None

        loc_stripped   = location.strip()
        loc_lower      = loc_stripped.lower().strip(",. ")
        
        # Check in-memory geocode cache
        with WeatherService._geocode_cache_lock:
            if loc_lower in WeatherService._geocode_cache:
                return WeatherService._geocode_cache[loc_lower]

        forced_display = None

        # ── Indian state name detection ──────────────────────────────────────
        state_info = INDIAN_STATE_CAPITALS.get(loc_lower)
        if state_info:
            capital, display = state_info
            forced_display   = display
            search_query     = capital + ", India"
        else:
            search_query = loc_stripped

        # ── Geocoding API call ───────────────────────────────────────────────
        try:
            resp = requests.get(
                WeatherService.GEOCODING_URL,
                params={
                    "name":     search_query,
                    "count":    5,
                    "language": "en",
                    "format":   "json",
                },
                timeout=WeatherService.TIMEOUT,
            )
            resp.raise_for_status()
            results = resp.json().get("results") or []

            if not results:
                print(f"[WeatherService] No geocoding results for '{search_query}'")
                return None

            # Score each result against the original query tokens
            query_tokens = set(loc_lower.replace(",", " ").split())
            scored = sorted(
                results,
                key=lambda r: _score_result(r, query_tokens),
                reverse=True,
            )
            best = scored[0]

            # If a forced display name was set (state-level lookup), use it
            display = forced_display if forced_display else WeatherService._build_display(best, loc_stripped)

            coords = {
                "lat":     best.get("latitude"),
                "lon":     best.get("longitude"),
                "display": display,
            }
            
            with WeatherService._geocode_cache_lock:
                WeatherService._geocode_cache[loc_lower] = coords
            return coords

        except Exception as e:
            print(f"[WeatherService] Geocoding failed for '{location}': {e}")
            return None

    @staticmethod
    def fetch_live_weather(location: str):
        """
        Fetch current weather for a location string.

        Returns a structured dict:
        {
            "location":          str,   # resolved place name + country
            "temperature_c":     float, # 2 m air temperature (degrees C)
            "feels_like_c":      float, # apparent temperature (degrees C)
            "humidity_pct":      int,   # relative humidity (%)
            "precipitation_mm":  float, # precipitation in last hour (mm)
            "wind_speed_kmh":    float, # wind speed at 10 m (km/h)
            "wind_direction":    int,   # wind direction (degrees)
            "uv_index":          float, # UV index
            "weather_code":      int,   # WMO weather code
            "condition":         str,   # human-readable condition
            "is_day":            bool,  # True = daytime
        }
        Returns None if anything fails.
        """
        coords = WeatherService.geocode(location)
        if not coords:
            return None

        # Check weather cache
        lat = coords["lat"]
        lon = coords["lon"]
        cache_key = (round(lat, 4), round(lon, 4))
        now = time.time()

        with WeatherService._weather_cache_lock:
            if cache_key in WeatherService._weather_cache:
                timestamp, cached_data = WeatherService._weather_cache[cache_key]
                if now - timestamp < WeatherService.WEATHER_CACHE_DURATION:
                    # Return cached copy but ensure location reflects query display name
                    result_copy = cached_data.copy()
                    result_copy["location"] = coords["display"]
                    return result_copy

        try:
            params = {
                "latitude":      coords["lat"],
                "longitude":     coords["lon"],
                "current":       (
                    "temperature_2m,apparent_temperature,relative_humidity_2m,"
                    "precipitation,wind_speed_10m,wind_direction_10m,"
                    "uv_index,weather_code,is_day"
                ),
                "timezone":      "auto",
                "forecast_days": 1,
            }
            resp = requests.get(
                WeatherService.WEATHER_URL,
                params=params,
                timeout=WeatherService.TIMEOUT,
            )
            resp.raise_for_status()
            data  = resp.json()
            cur   = data.get("current", {})
            wcode = int(cur.get("weather_code", 0))

            weather_data = {
                "location":         coords["display"],
                "temperature_c":    round(float(cur.get("temperature_2m",       0.0)), 1),
                "feels_like_c":     round(float(cur.get("apparent_temperature", 0.0)), 1),
                "humidity_pct":     int(cur.get("relative_humidity_2m",         0)),
                "precipitation_mm": round(float(cur.get("precipitation",        0.0)), 1),
                "wind_speed_kmh":   round(float(cur.get("wind_speed_10m",       0.0)), 1),
                "wind_direction":   int(cur.get("wind_direction_10m",            0)),
                "uv_index":         round(float(cur.get("uv_index",             0.0)), 1),
                "weather_code":     wcode,
                "condition":        WMO_CODE_DESCRIPTIONS.get(wcode, "Unknown"),
                "is_day":           bool(cur.get("is_day", 1)),
            }
            
            with WeatherService._weather_cache_lock:
                WeatherService._weather_cache[cache_key] = (now, weather_data)
            return weather_data
        except Exception as e:
            print(f"[WeatherService] Weather fetch failed for '{location}': {e}")
            return None

    @staticmethod
    def fetch_live_weather_by_coords(lat: float, lon: float, display_name: str = "Detected Location"):
        cache_key = (round(lat, 4), round(lon, 4))
        now = time.time()

        with WeatherService._weather_cache_lock:
            if cache_key in WeatherService._weather_cache:
                timestamp, cached_data = WeatherService._weather_cache[cache_key]
                if now - timestamp < WeatherService.WEATHER_CACHE_DURATION:
                    result_copy = cached_data.copy()
                    result_copy["location"] = display_name
                    return result_copy

        try:
            params = {
                "latitude":      lat,
                "longitude":     lon,
                "current":       (
                    "temperature_2m,apparent_temperature,relative_humidity_2m,"
                    "precipitation,wind_speed_10m,wind_direction_10m,"
                    "uv_index,weather_code,is_day"
                ),
                "timezone":      "auto",
                "forecast_days": 1,
            }
            resp = requests.get(
                WeatherService.WEATHER_URL,
                params=params,
                timeout=WeatherService.TIMEOUT,
            )
            resp.raise_for_status()
            data  = resp.json()
            cur   = data.get("current", {})
            wcode = int(cur.get("weather_code", 0))

            weather_data = {
                "location":         display_name,
                "temperature_c":    round(float(cur.get("temperature_2m",       0.0)), 1),
                "feels_like_c":     round(float(cur.get("apparent_temperature", 0.0)), 1),
                "humidity_pct":     int(cur.get("relative_humidity_2m",         0)),
                "precipitation_mm": round(float(cur.get("precipitation",        0.0)), 1),
                "wind_speed_kmh":   round(float(cur.get("wind_speed_10m",       0.0)), 1),
                "wind_direction":   int(cur.get("wind_direction_10m",            0)),
                "uv_index":         round(float(cur.get("uv_index",             0.0)), 1),
                "weather_code":     wcode,
                "condition":        WMO_CODE_DESCRIPTIONS.get(wcode, "Unknown"),
                "is_day":           bool(cur.get("is_day", 1)),
            }
            
            with WeatherService._weather_cache_lock:
                WeatherService._weather_cache[cache_key] = (now, weather_data)
            return weather_data
        except Exception as e:
            print(f"[WeatherService] Weather fetch by coords failed: {e}")
            return None

    @staticmethod
    def geocode_ip(ip: str):
        if not ip or ip in ("127.0.0.1", "::1", "localhost"):
            return None
        try:
            resp = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if not data.get("error"):
                    city = data.get("city") or ""
                    region = data.get("region") or ""
                    country = data.get("country_name") or ""
                    parts = [p for p in (city, region, country) if p]
                    display = ", ".join(parts) or "Detected Location"
                    return {
                        "lat": data.get("latitude"),
                        "lon": data.get("longitude"),
                        "display": display
                    }
        except Exception as e:
            print(f"[WeatherService] ipapi.co geocode failed for IP {ip}: {e}")

        try:
            resp = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == "success":
                    city = data.get("city") or ""
                    region = data.get("regionName") or ""
                    country = data.get("country") or ""
                    parts = [p for p in (city, region, country) if p]
                    display = ", ".join(parts) or "Detected Location"
                    return {
                        "lat": data.get("lat"),
                        "lon": data.get("lon"),
                        "display": display
                    }
        except Exception as e:
            print(f"[WeatherService] ip-api.com geocode failed for IP {ip}: {e}")

        return None
