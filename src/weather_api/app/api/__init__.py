from flask import Blueprint
from flask_restx import Api
from .weather import ns
from .auth import ns_auth
from .user import ns_user
from .history import ns_history

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

namespaces = [ns, ns_auth, ns_user, ns_history]

for namespace in namespaces:
    api.add_namespace(namespace)