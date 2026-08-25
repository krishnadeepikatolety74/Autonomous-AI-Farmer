import os
import json
import threading

# Path to the stats file inside the instance directory
STATS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance', 'api_usage_stats.json'))
_lock = threading.Lock()

def get_api_usage():
    """Retrieve the current API call counts."""
    with _lock:
        if not os.path.exists(STATS_FILE):
            # Create instance dir if not exists
            os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
            with open(STATS_FILE, 'w') as f:
                json.dump({"groq_calls": 0, "gemini_calls": 0}, f)
            return {"groq_calls": 0, "gemini_calls": 0}
        
        try:
            with open(STATS_FILE, 'r') as f:
                data = json.load(f)
                # Ensure keys are present
                if "groq_calls" not in data:
                    data["groq_calls"] = 0
                if "gemini_calls" not in data:
                    data["gemini_calls"] = 0
                return data
        except Exception:
            return {"groq_calls": 0, "gemini_calls": 0}

def increment_api_usage(provider):
    """Increment the API call counter for the specified provider."""
    with _lock:
        data = {"groq_calls": 0, "gemini_calls": 0}
        if os.path.exists(STATS_FILE):
            try:
                with open(STATS_FILE, 'r') as f:
                    data = json.load(f)
            except Exception:
                pass
        
        if "groq_calls" not in data:
            data["groq_calls"] = 0
        if "gemini_calls" not in data:
            data["gemini_calls"] = 0
            
        if provider == "groq":
            data["groq_calls"] += 1
        elif provider == "gemini":
            data["gemini_calls"] += 1
            
        os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
        with open(STATS_FILE, 'w') as f:
            json.dump(data, f)

def reset_api_usage():
    """Reset call counts back to 0."""
    with _lock:
        os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
        with open(STATS_FILE, 'w') as f:
            json.dump({"groq_calls": 0, "gemini_calls": 0}, f)
