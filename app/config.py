import os

DEBUG = True
SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')