import re

def validate_email(email):
    """Verify syntax of email address."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Verify password length requirements."""
    return len(password) >= 6

def validate_observation_input(data):
    """Ensure telemetry measurements fit normal physiological farming thresholds."""
    try:
        soil_moisture = float(data.get('soil_moisture', 0))
        soil_ph = float(data.get('soil_ph', 7))
        nitrogen = float(data.get('nitrogen', 0))
        phosphorus = float(data.get('phosphorus', 0))
        potassium = float(data.get('potassium', 0))
        temperature = float(data.get('temperature', 0))
        humidity = float(data.get('humidity', 0))
        rainfall = float(data.get('rainfall', 0))
        crop_health = float(data.get('crop_health', 100))
        
        # Ranges checks
        if not (0 <= soil_moisture <= 100): return False, "Soil moisture must be between 0% and 100%"
        if not (0 <= soil_ph <= 14): return False, "Soil pH must be between 0 and 14"
        if not (0 <= crop_health <= 100): return False, "Crop health index must be between 0% and 100%"
        if not (0 <= humidity <= 100): return False, "Humidity must be between 0% and 100%"
        
        return True, None
    except ValueError:
        return False, "All metric variables must be numerical numbers"
