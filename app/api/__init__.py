from flask import Blueprint
from flask_restx import Api
from .weather import ns
from .auth import ns_auth
from .user import ns_user

bp = Blueprint('api', __name__)

authorizations = {
    'jwt': {
        'type':'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type 'Bearer \<token>' in this field"
    }
}

description = """
This is a simple API that retrieves current and forecast weather data.
The data is retrieved from the OpenWeatherMap Database.
https://openweathermap.org/
"""

api = Api(
    bp,
    version='1.0', 
    title='Weather API',
    description=description,
    authorizations=authorizations,
    security='jwt',
    contact='Rafael Rodrigues Github',
    contact_url='https://github.com/rafaelrodrigues-dev',
)

api.add_namespace(ns, path='/api/v1')
api.add_namespace(ns_auth, path='/api/v1/auth')
api.add_namespace(ns_user, path='/api/v1/me')