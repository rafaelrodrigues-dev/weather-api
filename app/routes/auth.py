from flask import Blueprint,request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token
from app.models import User

bp_auth = Blueprint('auth', __name__)
jwt_manager = JWTManager()

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
    
    access_token = create_access_token(identity={
        'id':user.id,
        'email': user.email,
        'name':user.name
    })

    return jsonify(access_token), 200
