from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from app.models import User

def login_user(email: str = 'test@email.com',password : str = 'testPassw0rd'):
    """"The function creates a user and returns the user object along with an access token."""
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