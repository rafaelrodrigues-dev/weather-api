from flask import Blueprint,jsonify, request
from app.services import get_current_weather, get_forecast_weather

bp_main = Blueprint('main',__name__)

@bp_main.route('/api/v1/weather', methods=['GET'])
def weather():
    city = request.args.get('city')

    if not city:
        return jsonify({"error": "Parameter city is required"}), 400

    weather_data = get_current_weather(city)

    if weather_data:
        return weather_data
    else:
        return jsonify({"error": "Unable to obtain weather data"}), 404

@bp_main.route('/api/v1/forecast', methods=['GET'])
def forecast():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Parameter city is required"}), 400
    
    forecast_data = get_forecast_weather(city)

    if forecast_data:
        return forecast_data
    else:
        return jsonify({"error": "Unable to obtain weather forecast data"}), 404