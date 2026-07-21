import requests
import platform
import os

def send_anonymous_telemetry():
    URL_CLOUDFLARE = "https://telemetry-weather-api.rafaelrodriguesrr06.workers.dev/"
    
    payload = {
        "os": platform.system(),
        "python_version": platform.python_version(),
        "project": "weather-api"
    }

    try:
        requests.post(URL_CLOUDFLARE, json=payload, timeout=3)
    except requests.RequestException:
        pass

def start_telemetry():
    if os.getenv("ENVIRONMENT") == "development":
        return
        
    send_anonymous_telemetry()
