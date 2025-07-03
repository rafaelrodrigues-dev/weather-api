from flask_jwt_extended import create_access_token
from app.models import User, Weather
from werkzeug.security import generate_password_hash

def login_user(email='test@email.com',password='testPassw0rd'):
    # Create a user in the database
    hashed_password = generate_password_hash(password)
    User(name='Test User', password=hashed_password,email=email).create()
    user = User.query.filter_by(email=email).first()

    # Create an access token for the user
    access_token = create_access_token(identity=str(user.id))

    # Return the user and access token
    return {
        'user': user,
        'access_token': access_token
    }

def test_api_v1_weather(client):
    """Test the /api/v1/weather endpoint."""
    logged_user = login_user()
    response = client.get(
        '/api/v1/weather',
        query_string={'city': 'belo horizonte'},
        headers={'Authorization': f'Bearer {logged_user['access_token']}'}
    )
    assert b'weather' in response.data
    assert b'temp' in response.data
    assert b'humidity' in response.data
    assert b'description' in response.data
    assert response.status_code == 200

def test_api_v1_weather_no_city(client):
    """Test the /api/v1/weather endpoint without city parameter."""
    logged_user = login_user()
    response = client.get(
        '/api/v1/weather',
        headers={'Authorization': f'Bearer {logged_user['access_token']}'
    })
    assert b'Parameter city is required' in response.data
    assert response.status_code == 400

def test_api_v1_weather_invalid_city(client):
    """Test the /api/v1/weather endpoint with an invalid city"""
    logged_user = login_user()
    response = client.get(
        '/api/v1/weather',
        query_string={'city': 'invalidcity'},
        headers={'Authorization': f'Bearer {logged_user['access_token']}'}
    )

    assert b'Unable to obtain weather data' in response.data
    assert response.status_code == 404

def test_api_v1_forecast(client):
    """Test the /api/v1/forecast endpoint."""
    logged_user = login_user()
    response = client.get(
        '/api/v1/forecast',
        query_string={'city': 'belo horizonte'},
        headers={'Authorization': f'Bearer {logged_user['access_token']}'}
    )
    assert b'weather' in response.data
    assert b'temp' in response.data
    assert b'humidity' in response.data
    assert b'description' in response.data
    assert response.status_code == 200

def test_api_v1_forecast_no_city(client):
    """Test the /api/v1/forecast endpoint without city parameter."""
    logged_user = login_user()
    response = client.get(
        '/api/v1/forecast',
        headers={'Authorization': f'Bearer {logged_user['access_token']}'}
    )

    assert b'Parameter city is required' in response.data
    assert response.status_code == 400

def test_api_v1_forecast_invalid_city(client):
    """Test the /api/v1/forecast endpoint with an invalid city"""
    logged_user = login_user()
    response = client.get(
        '/api/v1/forecast',
        query_string={'city': 'invalidcity'},
        headers={'Authorization': f'Bearer {logged_user['access_token']}'}
    )

    assert b'Unable to obtain weather forecast data' in response.data
    assert response.status_code == 404

def test_api_v1_me(client):
    """Test the /api/v1/me endpoint."""
    logged_user = login_user()
    response = client.get('/api/v1/me', headers={'Authorization': f'Bearer {logged_user['access_token']}'})
    
    assert b'1' in response.data
    assert b'test@email.com' in response.data
    assert response.status_code == 200

def test_api_v1_history_shows_weather_history(client):
    """Test the /api/v1/history endpoint."""
    logged_user = login_user()

    for i in range(5):
        Weather(
            city=f'City {i}',
            temperature=25.0,
            feels_like=24.0,
            humidity=60.0,
            description='Sunny',
            user=logged_user['user']
        ).create()

    response = client.get('/api/v1/history', headers={'Authorization': f'Bearer {logged_user['access_token']}'})

    for i in range(5):
        assert f'City {i}'.encode() in response.data

    assert b'Sunny' in response.data
    assert b'25.0' in response.data
    assert b'60.0' in response.data
