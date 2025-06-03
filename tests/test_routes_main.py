from flask_jwt_extended import create_access_token
from app.models import User
from werkzeug.security import generate_password_hash

def test_weather(client):
    """Test the /api/v1/weather endpoint."""
    response = client.get('/api/v1/weather', query_string={'city': 'belo horizonte'})
    assert b'weather' in response.data
    assert b'temp' in response.data
    assert b'humidity' in response.data
    assert b'description' in response.data
    assert response.status_code == 200

def test_weather_no_city(client):
    """Test the /api/v1/weather endpoint without city parameter."""
    response = client.get('/api/v1/weather')
    assert b'Parameter city is required' in response.data
    assert response.status_code == 400

def test_weather_invalid_city(client):
    """Test the /api/v1/weather endpoint with an invalid city"""
    response = client.get('/api/v1/weather', query_string={'city': 'invalidcity'})
    assert b'Unable to obtain weather data' in response.data
    assert response.status_code == 404

def test_forecast(client):
    """Test the /api/v1/forecast endpoint."""
    response = client.get('/api/v1/forecast', query_string={'city': 'belo horizonte'})
    assert b'weather' in response.data
    assert b'temp' in response.data
    assert b'humidity' in response.data
    assert b'description' in response.data
    assert response.status_code == 200

def test_forecast_no_city(client):
    """Test the /api/v1/forecast endpoint without city parameter."""
    response = client.get('/api/v1/forecast')
    assert b'Parameter city is required' in response.data
    assert response.status_code == 400

def test_forecast_invalid_city(client):
    """Test the /api/v1/forecast endpoint with an invalid city"""
    response = client.get('/api/v1/forecast', query_string={'city': 'invalidcity'})
    assert b'Unable to obtain weather forecast data' in response.data
    assert response.status_code == 404

def test_me(client):
    """Test the /api/v1/me endpoint."""
    # Create a user in the database
    password = 'testpassword'
    email = 'test@email.com'
    hashed_password = generate_password_hash(password)
    User(name='Test User', password=hashed_password,email=email).create()
    user = User.query.filter_by(email=email).first()
    # Create an access token for the user
    access_token = create_access_token(identity=str(user.id))

    response = client.get('/api/v1/me', headers={'Authorization': f'Bearer {access_token}'})
    
    assert b'1' in response.data
    assert b'test@email.com' in response.data
    assert response.status_code == 200