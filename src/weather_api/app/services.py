import os
import requests

API_KEY = os.environ.get('API_KEY','')

def get_current_weather(city,lang):
    if not API_KEY:
        raise ValueError("API_KEY is not set. Please set the API_KEY environment variable.")
    
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang={lang}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_forecast_weather(city,lang):
    if not API_KEY:
        raise ValueError("API_KEY is not set. Please set the API_KEY environment variable.")
    
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang={lang}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None