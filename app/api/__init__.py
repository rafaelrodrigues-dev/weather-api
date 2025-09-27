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

api = Api(
    bp,
    version='1.0', 
    title='Weather API',
    description='A simple API to get weather data',
    authorizations=authorizations,
    security='jwt'
)

api.add_namespace(ns, path='/api/v1')
api.add_namespace(ns_auth, path='/api/v1/auth')
api.add_namespace(ns_user, path='/api/v1/me')