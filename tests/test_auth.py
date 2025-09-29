from app.models import User
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_refresh_token

def test_register_successful(client):
    # Test successful registration
    response = client.post('/api/v1/auth/register', json={
        'name': 'Test User',
        'password': 'Passw0rd',
        'email': 'test@email.com'
    })
    user = User.query.filter_by(email='test@email.com').first()

    # Check if the response contains the expected message
    assert b'User created' in response.data
    assert response.status_code == 201

    # Check if user was created in the database
    assert user.name == 'Test User'

    # Password should be hashed
    assert user.password != 'testpassword'

def test_register_missing_fields(client):
    # Test missing fields
    response = client.post('/api/v1/auth/register', json={
    })
    assert b'Missing required fields' in response.data
    assert response.status_code == 400

def test_register_email_exists(client):
    # Test email already exists
    User(name='Test User', password='password',email='test@email.com').create()

    response = client.post('/api/v1/auth/register', json={
        'name': 'Test User',
        'password': 'Passw0rd',
        'email': 'test@email.com'
    })

    assert b'Email already exists' in response.data
    assert response.status_code == 400

def test_register_invalid_email(client):
    response = client.post('/api/v1/auth/register', json={
        'name': 'Test User',
        'password': 'Passw0rd',
        'email': 'test@email@invalid.com'
    })

    assert b'Email is not valid' in response.data
    assert response.status_code == 400

def test_register_password_is_too_weak(client):
    response = client.post('/api/v1/auth/register', json={
        'name':'Test User',
        'password': 'password',
        'email': 'test@email.com'
    })
    
    assert b'Password is too weak' in response.data
    assert b'Password must be alphanumeric, one uppercase and one lowercase.' in response.data
    assert response.status_code == 400

def test_login_successful(client):
    # Test successful login
    password = 'Passw0rd'
    hashed_password = generate_password_hash(password)
    # Create a user in the database
    User(name='Test User', password=hashed_password,email='test@email.com').create()
    response = client.post('/api/v1/auth/login', json={
        'email': 'test@email.com',
        'password': password,
    })

    assert b'access_token' in response.data
    assert b'refresh_token' in response.data
    assert response.status_code == 200

def test_login_missing_fields(client):
    # Test missing fields
    response = client.post('/api/v1/auth/login', json={})
    assert b'Missing required fields' in response.data
    assert response.status_code == 400

def test_login_invalid_credentials(client):
    # Test invalid credentials
    response = client.post('/api/v1/auth/login', json={
        'email': 'testinvalid@email.com',
        'password': 'wrongpassword',
    })
    assert b'Credentials invalid' in response.data
    assert response.status_code == 401

def test_refresh_token_successful(client):
    # Test successful token refresh
    password = 'Passw0rd'
    hashed_password = generate_password_hash(password)
    # Create a user in the database
    User(name='Test User',email='test@email.com', password=hashed_password).create()
    user = User.query.filter_by(email='test@email.com').first()
    # Create a refresh token for the user
    refresh_token = create_refresh_token(identity=str(user.id))
    response = client.post('/api/v1/auth/refresh', headers={
        'Authorization': f'Bearer {refresh_token}'
    })
    
    assert b'access_token' in response.data
    assert response.status_code == 200