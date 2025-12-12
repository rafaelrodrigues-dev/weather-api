import json
from app.models import Weather
from tests.utils import login_user

def test_get_weather_history(client):
    """Test getting weather history for logged-in user."""
    logged_user = login_user()
    # Create some weather history entries
    for i in range(5):
        Weather(user_id=logged_user['user'].id, data={'city': f'city{i}', 'temp': 20 + i}).create()

    headers = {'Authorization': f'Bearer {logged_user["access_token"]}'}
    response = client.get('/api/v1/history/', headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'calls' in data
    assert len(data['calls']) == 5
    assert data['page'] == 1
    assert data['pages'] == 1
    assert data['total'] == 5
    # Check order: most recent first
    assert data['calls'][0]['data']['city'] == 'city4'

def test_get_weather_history_pagination(client):
    """Test pagination in weather history."""
    logged_user = login_user()
    # Create 11 entries
    for i in range(11):
        Weather(user_id=logged_user['user'].id, data={'city': f'city{i}', 'temp': 20 + i}).create()

    headers = {'Authorization': f'Bearer {logged_user["access_token"]}'}
    response = client.get('/api/v1/history/', query_string={'page': 1}, headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['calls']) == 10
    assert data['page'] == 1
    assert data['pages'] == 2
    assert data['total'] == 11

    response2 = client.get('/api/v1/history/', query_string={'page': 2}, headers=headers)
    assert response2.status_code == 200
    data2 = json.loads(response2.data)
    assert len(data2['calls']) == 1
    assert data2['page'] == 2

def test_get_weather_history_empty(client):
    """Test getting weather history when empty."""
    logged_user = login_user()
    headers = {'Authorization': f'Bearer {logged_user["access_token"]}'}
    response = client.get('/api/v1/history/', headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['calls'] == []
    assert data['total'] == 0

def test_get_weather_history_unauthorized(client):
    """Test getting weather history without authorization."""
    response = client.get('/api/v1/history/')
    assert response.status_code == 401

def test_get_weather_history_user_not_found(client):
    """Test getting weather history for non-existent user."""
    logged_user = login_user()
    logged_user['user'].delete()
    headers = {'Authorization': f'Bearer {logged_user["access_token"]}'}
    response = client.get('/api/v1/history/', headers=headers)
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'User not found' in data['message']

def test_delete_weather_history(client):
    """Test deleting weather history for logged-in user."""
    logged_user = login_user()
    # Create some history
    for i in range(3):
        Weather(user_id=logged_user['user'].id, data={'city': f'city{i}'}).create()

    headers = {'Authorization': f'Bearer {logged_user["access_token"]}'}
    response = client.delete('/api/v1/history/', headers=headers)
    assert response.status_code == 204

    # Check if deleted
    history = Weather.query.filter_by(user_id=logged_user['user'].id).all()
    assert len(history) == 0

def test_delete_weather_history_unauthorized(client):
    """Test deleting weather history without authorization."""
    response = client.delete('/api/v1/history/')
    assert response.status_code == 401

def test_delete_weather_history_user_not_found(client):
    """Test deleting weather history for non-existent user."""
    logged_user = login_user()
    logged_user['user'].delete()
    headers = {'Authorization': f'Bearer {logged_user["access_token"]}'}
    response = client.delete('/api/v1/history/', headers=headers)
    assert response.status_code == 404
