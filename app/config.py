import os
from datetime import timedelta

SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL','sqlite:///db.sqlite3')
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ACESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
SWAGGER_UI_DOC_EXPANSION = 'list'
SWAGGER_UI_OPERATION_ID = True