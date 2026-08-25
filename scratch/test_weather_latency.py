import sys
import os
import time

# Ensure base directory is on path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_dir)

from app import create_app
from services.weather_service import WeatherService

def test_weather_latency():
    print("==================================================")
    print("       WEATHER SERVICE LATENCY VERIFICATION       ")
    print("==================================================")

    app = create_app()
    with app.app_context():
        location = "Hyderabad"
        print(f"Location to test: {location}\n")

        # First Call (Cache Miss / Live Fetch)
        print("--- Call 1: Live Fetch (Cache Miss) ---")
        start1 = time.time()
        res1 = WeatherService.fetch_live_weather(location)
        elapsed1 = time.time() - start1
        
        if res1:
            print(f"Resolved Location: {res1.get('location')}")
            print(f"Temperature: {res1.get('temperature_c')}°C, Condition: {res1.get('condition')}")
            print(f"Time taken: {elapsed1:.4f} seconds")
        else:
            print("ERROR: Failed to fetch weather on first call.")
            sys.exit(1)

        # Second Call (Cache Hit)
        print("\n--- Call 2: Cached Fetch (Cache Hit) ---")
        start2 = time.time()
        res2 = WeatherService.fetch_live_weather(location)
        elapsed2 = time.time() - start2
        
        if res2:
            print(f"Resolved Location: {res2.get('location')}")
            print(f"Temperature: {res2.get('temperature_c')}°C, Condition: {res2.get('condition')}")
            print(f"Time taken: {elapsed2:.4f} seconds")
        else:
            print("ERROR: Failed to fetch weather on second call.")
            sys.exit(1)

        # Verification assertion
        speedup = elapsed1 / elapsed2 if elapsed2 > 0 else float('inf')
        print(f"\nCache Speedup Factor: {speedup:.2f}x")
        
        assert elapsed2 < 0.010, f"Cached call took too long: {elapsed2:.4f} seconds"
        print("\nVERIFICATION SUCCESS: Caching is active and working as expected!")
        print("==================================================")

if __name__ == "__main__":
    test_weather_latency()
