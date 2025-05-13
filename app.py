import os
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

API_KEY = os.environ.get('API_KEY','')

def get_current_weather(city):
    if not API_KEY:
        raise ValueError("API_KEY is not set. Please set the API_KEY environment variable.")
    
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=pt'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_forecast_weather(city):
    if not API_KEY:
        raise ValueError("API_KEY is not set. Please set the API_KEY environment variable.")
    
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=pt'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.route('/api/v1/weather', methods=['GET'])
def weather():
    city = request.args.get('city')

    if not city:
        return jsonify({"error": "Parameter city is required"}), 400

    weather_data = get_current_weather(city)

    if weather_data:
        return weather_data
    else:
        return jsonify({"error": "Unable to obtain weather data"}), 404
    
@app.route('/api/v1/forecast', methods=['GET'])
def forecast():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Parameter city is required"}), 400
    
    forecast_data = get_forecast_weather(city)

    if forecast_data:
        return forecast_data
    else:
        return jsonify({"error": "Unable to obtain forecast data"}), 404

if __name__ == '__main__':
    app.run(debug=True)