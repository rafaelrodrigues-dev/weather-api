import os
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

def create_app(config_path):
    app = Flask(__name__)
    app.config.from_pyfile(config_path)

    CORS(app)
    Swagger(app, template_file=os.path.join(os.path.dirname(__file__),'docs', 'swagger.yml'))

    from app.routes.main import bp_main
    app.register_blueprint(bp_main)

    return app