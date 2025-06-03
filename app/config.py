import os
from datetime import timedelta

SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ACESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)