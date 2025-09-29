import json
from werkzeug.security import check_password_hash
from app.models import User
from tests.utils import login_user

def test_get_user_info(client):
    """
    Test case for successfully retrieving the logged-in user's information.
    """
    user_logged = login_user()
    headers = {
        'Authorization': f'Bearer {user_logged['access_token']}'
    }
    response = client.get('/api/v1/me/', headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'user' in data
    assert data['user']['email'] == user_logged['user'].email
    assert data['user']['name'] == user_logged['user'].name

def test_get_user_info_unauthorized(client):
    """
    Test case for attempting to retrieve user info without authentication.
    """
    response = client.get('/api/v1/me/')
    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'msg' in data
    assert data['msg'] == 'Missing Authorization Header'

def test_get_user_not_found(client):
    """
    Test case for attempting to retrieve user info with a non-existent user.
    """
    user_logged = login_user()
    user_logged['user'].delete()
    headers = {
        'Authorization': f'Bearer {user_logged['access_token']}',
        'Content-Type': 'application/json'
    }
    response = client.get('/api/v1/me/',headers=headers)
    data = json.loads(response.data)
    assert 'User not found' in data['message']

def test_update_user_name(client):
    """
    Test case for successfully updating the user's name.
    """
    user_logged = login_user()
    headers = {
        'Authorization': f'Bearer {user_logged['access_token']}',
        'Content-Type': 'application/json'
    }
    payload = {'name': 'Updated Test User'}
    response = client.patch('/api/v1/me/', headers=headers, data=json.dumps(payload))
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['msg'] == 'User updated'
    
    user = User.query.filter_by(id=user_logged['user'].id).first()
    assert user.name == 'Updated Test User'

def test_update_user_email(client):
    """
    Test case for successfully updating the user's email.
    """
    user_logged = login_user()
    headers = {
        'Authorization': f'Bearer {user_logged['access_token']}',
        'Content-Type': 'application/json'
    }
    payload = {'email': 'newemail@example.com'}
    response = client.patch('/api/v1/me/', headers=headers, data=json.dumps(payload))
    assert response.status_code == 200
    
    user = User.query.filter_by(id=user_logged['user'].id).first()
    assert user.email == 'newemail@example.com'

def test_update_user_password(client):
    """
    Test case for successfully updating the user's password.
    """
    user_logged = login_user()
    headers = {
        'Authorization': f'Bearer {user_logged['access_token']}',
        'Content-Type': 'application/json'
    }
    new_password = 'NewSecurePassword123'
    payload = {'password': new_password}
    response = client.patch('/api/v1/me/', headers=headers, data=json.dumps(payload))
    assert response.status_code == 200
    
    user = User.query.filter_by(id=user_logged['user'].id).first()
    assert check_password_hash(user.password, new_password)

def test_update_user_invalid_email(client):
    """
    Test case for attempting to update with an invalid email format.
    """
    user_logged = login_user()
    headers = {
        'Authorization': f'Bearer {user_logged['access_token']}',
        'Content-Type': 'application/json'
    }
    payload = {'email': 'invalid-email'}
    response = client.patch('/api/v1/me/', headers=headers, data=json.dumps(payload))
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['msg'] == 'Invalid email format'

def test_update_user_weak_password(client):
    """
    Test case for attempting to update with a weak password.
    """
    user_logged = login_user()
    headers = {
        'Authorization': f'Bearer {user_logged['access_token']}',
        'Content-Type': 'application/json'
    }
    payload = {'password': 'weak'}
    response = client.patch('/api/v1/me/', headers=headers, data=json.dumps(payload))
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['msg'] == 'Password is too weak'

def test_update_user_no_data_to_update(client):
    """
    Test case for attempting to update with no data provided.
    """
    user_logged = login_user()
    headers = {
        'Authorization': f'Bearer {user_logged['access_token']}',
        'Content-Type': 'application/json'
    }
    payload = {}
    response = client.patch('/api/v1/me/', headers=headers, data=json.dumps(payload))
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['msg'] == 'No data provided to update'

def test_update_user_invalid_data_to_update(client):
    """
    Test case for attempting to update with no data provided.
    """
    user_logged = login_user()
    headers = {
        'Authorization': f'Bearer {user_logged['access_token']}',
        'Content-Type': 'application/json'
    }
    payload = {'something':'abracadabra'}
    response = client.patch('/api/v1/me/', headers=headers, data=json.dumps(payload))
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['msg'] == 'No valid data provided to update'

def test_delete_user(client):
    """
    Test case for successfully deleting a user.
    """
    user_logged = login_user()
    headers = {
        'Authorization': f'Bearer {user_logged['access_token']}'
    }
    response = client.delete('/api/v1/me/', headers=headers)
    assert response.status_code == 204
    
    user = User.query.filter_by(id=user_logged['user'].id).first()
    assert user is None


def test_delete_user_unauthorized(client):
    """
    Test case for attempting to delete a user without authentication.
    """
    response = client.delete('/api/v1/me/')
    assert response.status_code == 401