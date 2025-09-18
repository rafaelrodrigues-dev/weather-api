from flask import request, current_app
from flask_restx import Resource, Namespace
from app.services import get_current_weather, get_forecast_weather
from flask_jwt_extended import jwt_required
import json

ns = Namespace('Weather', description='Weather operations')

@ns.route('/weather')
@ns.param('city', 'name of the city', required=True)
@ns.param('lang', 'language code for the response', required=False, default='en')
@ns.response(404, 'City not found')
class WeatherResource(Resource):
    method_decorators = [jwt_required()]

    @ns.doc('Get current weather data for a city')
    def get(self):
        city = request.args.get('city')
        lang = request.args.get('lang', 'en')
        if not city:
            return {'msg': 'Parameter city is required'}, 400
        
        cache_key = f'weather:{city.lower()}'
        cached_data = current_app.redis.get(cache_key)
        if cached_data:
            return json.loads(cached_data), 200

        weather_data = get_current_weather(city,lang)

        if weather_data:
            # Cache the weather data for 10 minutes
            current_app.redis.setex(cache_key, 600, json.dumps(weather_data))
            return weather_data
        else:
            return {'msg': 'Unable to obtain weather data'}, 404

@ns.route('/forecast')
@ns.param('city', 'name of the city', required=True)
@ns.param('lang', 'language code for the response', required=False, default='en')
class ForecastResource(Resource):
    method_decorators = [jwt_required()]

    @ns.doc('Get weather forecast data for a city')
    def get(self):
        city = request.args.get('city')
        lang = request.args.get('lang', 'en')
        if not city:
            return {'msg': 'Parameter city is required'}, 400
        
        cache_key= f'forecast:{city.lower()}'
        cached_data = current_app.redis.get(cache_key)
        if cached_data:
            return json.loads(cached_data), 200

        forecast_data = get_forecast_weather(city,lang)

        if forecast_data:
            return forecast_data
        else:
            return {'msg': 'Unable to obtain weather forecast data'}, 404
