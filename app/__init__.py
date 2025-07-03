import os
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
import redis

from dotenv import load_dotenv

def create_app(config_path='config.py'):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_pyfile(config_path)

    app.redis = redis.StrictRedis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        db=int(os.getenv('REDIS_DB', 0)),
        decode_responses=True
    )

    CORS(app)
    Swagger(app, template_file=os.path.join(os.path.dirname(__file__),'docs', 'swagger.yml'))

    from app.models import db, migrate
    db.init_app(app)
    migrate.init_app(app,db)

    from app.routes.auth import bp_auth, jwt_manager
    jwt_manager.init_app(app)
    app.register_blueprint(bp_auth)

    from app.routes.main import bp_main
    app.register_blueprint(bp_main)

    return app