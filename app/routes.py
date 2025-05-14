import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger
from .services import get_current_weather, get_forecast_weather

app = Flask(__name__)
CORS(app)
swagger = Swagger(app, template_file=os.path.join(os.path.dirname(__file__), 'docs/swagger.yml'))

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