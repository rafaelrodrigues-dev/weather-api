from flask import Blueprint,jsonify, request
from app.services import get_current_weather, get_forecast_weather
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Weather

bp_main = Blueprint('main',__name__)

@bp_main.route('/api/v1/weather', methods=['GET'])
@jwt_required()
def weather():
    city = request.args.get('city')

    if not city:
        return jsonify({"error": "Parameter city is required"}), 400

    weather_data = get_current_weather(city)

    if weather_data:
        # Save the weather data to the database
        current_user_id = get_jwt_identity()
        main_data = {
            'city': weather_data.get('name'),
            'temperature': weather_data.get('main').get('temp'),
            'feels_like': weather_data.get('main').get('feels_like'),
            'humidity': weather_data.get('main').get('humidity'),
            'description': weather_data.get('weather')[0].get('description'),
            'user': User.query.filter_by(id=current_user_id).first()
        }
        Weather(**main_data).create()

        return weather_data
    else:
        return jsonify({"error": "Unable to obtain weather data"}), 404

@bp_main.route('/api/v1/forecast', methods=['GET'])
@jwt_required()
def forecast():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Parameter city is required"}), 400
    
    forecast_data = get_forecast_weather(city)

    if forecast_data:
        return forecast_data
    else:
        return jsonify({"error": "Unable to obtain weather forecast data"}), 404

@bp_main.route('/api/v1/me',methods=['GET'])
@jwt_required()
def me():
    # Page where the user can see their data 
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).first()
    user_data = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
    }

    return jsonify(user_data), 200

@bp_main.route('/api/v1/history', methods=['GET'])
@jwt_required()
def history():
    # Page where the user can see their history
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).first()

    # Paginate the user's history
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page',10, type=int)
    paginated_history = user.history.paginate(page=page, per_page=per_page, error_out=False)
    history_items = [
        {
            'city': weather_data.city,
            'temperature': weather_data.temperature,
            'feels_like': weather_data.feels_like,
            'humidity': weather_data.humidity,
            'description': weather_data.description,
            'generated_at': weather_data.generated_at
        }
        for weather_data in paginated_history.items
    ]
    history_data = {
        'history': history_items,
        'total': paginated_history.total,
        'pages': paginated_history.pages,
        'current_page':paginated_history.page,
    }

    return jsonify(history_data), 200