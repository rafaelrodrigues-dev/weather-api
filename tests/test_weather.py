from tests.utils import login_user


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
