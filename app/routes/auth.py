from flask import Blueprint,request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity 
)
from app.models import User
from app.validators import validate_email, validate_password

jwt_manager = JWTManager()
bp_auth = Blueprint('auth', __name__)

@bp_auth.route('/api/v1/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')
    email = data.get('email')
    if not name or not password or not email:
        return jsonify({'msg': 'Missing required fields'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'msg': 'Email already exists'}), 400
    
    if not validate_email(email):
        return jsonify({'msg': 'Email is not valid'}), 400
    
    if not validate_password(password):
        return jsonify({
            'msg':'Password is too weak',
            'obs':'Password must be alphanumeric, one uppercase and one lowercase.'
        }), 400
    
    hashed_password = generate_password_hash(password)
    User(name=name, password=hashed_password, email=email).create()

    return jsonify({'msg': 'User created'}), 201

@bp_auth.route('/api/v1/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()

    if not email or not password:
        return jsonify({'msg': 'Missing required fields'}), 400
    
    elif not user or not check_password_hash(user.password,password):
        return jsonify({'msg': 'Credentials invalid'}), 401
    
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify(access_token=access_token,refresh_token=refresh_token), 200

@bp_auth.route('/api/v1/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200