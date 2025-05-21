import os
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

def create_app(config_path='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_path)

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