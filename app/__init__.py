import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import redis
from flask_jwt_extended import JWTManager

load_dotenv()

def create_app(config_path='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_path)

    app.redis = redis.Redis.from_url(os.getenv('REDIS_URL'))

    CORS(app)
    JWTManager(app)

    from app.models import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    from .api import bp
    app.register_blueprint(bp, url_prefix='/')

    return app