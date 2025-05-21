from app.models import User

def test_register(client):
    # Test successful registration
    response = client.post('/api/v1/auth/register', json={
        'name': 'Test User',
        'password': 'testpassword',
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
        'password': 'testpassword',
        'email': 'test@email.com'
    })

    assert b'Email already exists' in response.data
    assert response.status_code == 400