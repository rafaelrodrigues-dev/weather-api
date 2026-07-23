from tests.utils import login_user
from unittest.mock import patch

def test_api_v1_weather(client):
    """Test the /api/v1/weather endpoint."""
    logged_user = login_user()
    response = client.get(
        '/api/v1/weather',
        query_string={'city': 'belo horizonte'},
        headers={'Authorization': f'Bearer {logged_user['access_token']}'}
    )
    assert b'areaName' in response.data
    assert b'observation_time' in response.data
    assert b'temp_C' in response.data
    assert b'FeelsLikeC' in response.data
    assert b'weatherDesc' in response.data
    assert b'humidity' in response.data
    assert b'precipMM' in response.data
    assert b'uvIndex' in response.data
    assert b'windspeedKmph' in response.data
    assert b'winddir16Point' in response.data
    assert b'weatherIconUrl' in response.data
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

@patch('app.api.weather.current_app.redis')
@patch('app.api.weather.get_current_weather')
def test_api_v1_weather_cache_data(mock_get_current_weather, mock_redis, client):
    """Test the /api/v1/weather endpoint with cached data."""
    mock_redis.get.return_value = None
    mock_get_current_weather.return_value = {
        'weather': [{'description': 'céu limpo'}],
        'main': {'temp': 25, 'humidity': 60}
    }
    logged_user = login_user()
    headers = {'Authorization': f'Bearer {logged_user["access_token"]}'}
    query_string = {'city': 'cachedcity'}

    response1 = client.get('/api/v1/weather', query_string=query_string, headers=headers)
    assert response1.status_code == 200

    mock_redis.get.assert_called_once_with('weather:cachedcity')
    mock_get_current_weather.assert_called_once_with('cachedcity', 'en')
    mock_redis.setex.assert_called_once()

    mock_redis.get.return_value = response1.data.decode('utf-8')

    response2 = client.get('/api/v1/weather', query_string=query_string, headers=headers)
    assert response2.status_code == 200

    mock_get_current_weather.assert_called_once()

def test_api_v1_forecast(client):
    """Test the /api/v1/forecast endpoint."""
    logged_user = login_user()
    response = client.get(
        '/api/v1/forecast',
        query_string={'city': 'belo horizonte'},
        headers={'Authorization': f'Bearer {logged_user['access_token']}'}
    )
    assert b'areaName' in response.data
    assert b'date' in response.data
    assert b'avgtempC' in response.data
    assert b'mintempC' in response.data
    assert b'maxtempC' in response.data
    assert b'uvIndex' in response.data
    assert b'sunrise' in response.data
    assert b'sunset' in response.data
    assert b'hourly' in response.data

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

@patch('app.api.weather.current_app.redis')
@patch('app.api.weather.get_forecast_weather')
def test_api_v1_forecast_cache_data(mock_get_forecast_weather, mock_redis, client):
    """Test the /api/v1/forecast endpoint with cached data."""
    mock_redis.get.return_value = None
    mock_get_forecast_weather.return_value = {
        'weather': [{'description': 'céu limpo'}],
        'main': {'temp': 25, 'humidity': 60}
    }
    logged_user = login_user()
    headers = {'Authorization': f'Bearer {logged_user["access_token"]}'}
    query_string = {'city': 'cachedcity'}


    response1 = client.get('/api/v1/forecast', query_string=query_string, headers=headers)
    assert response1.status_code == 200
    
    mock_redis.get.assert_called_once_with('forecast:cachedcity')
    mock_get_forecast_weather.assert_called_once_with('cachedcity', 'en')
    mock_redis.setex.assert_called_once()

    mock_redis.get.return_value = response1.data.decode('utf-8')

    response2 = client.get('/api/v1/forecast', query_string=query_string, headers=headers)
    assert response2.status_code == 200

    mock_get_forecast_weather.assert_called_once()