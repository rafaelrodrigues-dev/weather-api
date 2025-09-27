from flask import request
from flask_restx import Resource, Namespace, fields
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, get_jwt_identity 
)
from app.models import User
from app.validators import validate_email, validate_password

ns_auth = Namespace('Auth', description='Authentication operations')

register_model = ns_auth.model('Register_User', {
    'name': fields.String(required=True, description='The user name'),
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password')
})

login_model = ns_auth.model('Login', {
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password')
})

@ns_auth.route('/register')
@ns_auth.response(400, 'Validation Error')
@ns_auth.response(201, 'User created successfully')
class RegisterResource(Resource):
    @ns_auth.doc('Register a new user',security=None)
    @ns_auth.expect(register_model)
    def post(self):
        data = request.get_json()
        name = data.get('name')
        password = data.get('password')
        email = data.get('email')
        if not name or not password or not email:
            return {'msg': 'Missing required fields'}, 400
        
        if User.query.filter_by(email=email).first():
            return {'msg': 'Email already exists'}, 400
        
        if not validate_email(email):
            return {'msg': 'Email is not valid'}, 400
        
        if not validate_password(password):
            return {
                'msg':'Password is too weak',
                'obs':'Password must be alphanumeric, one uppercase and one lowercase.'
            }, 400
        
        hashed_password = generate_password_hash(password)
        User(name=name, password=hashed_password, email=email).create()

        return {'msg': 'User created successfully'}, 201

@ns_auth.route('/login')
@ns_auth.response(400, 'Validation Error')
@ns_auth.response(401, 'Credentials invalid')
@ns_auth.response(200, 'Login successful')
class LoginResource(Resource):
    @ns_auth.doc('User login to obtain JWT tokens',security=None)
    @ns_auth.expect(login_model)
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()

        if not email or not password:
            return {'msg': 'Missing required fields'}, 400
        
        elif not user or not check_password_hash(user.password,password):
            return {'msg': 'Credentials invalid'}, 401
        
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return {'access_token':access_token,'refresh_token':refresh_token} ,200

@ns_auth.route('/refresh')
class RefreshResource(Resource):
    method_decorators = [jwt_required(refresh=True)]

    @ns_auth.doc('Obtain a new access token using a refresh token')
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return {'access_token':new_access_token}, 200
