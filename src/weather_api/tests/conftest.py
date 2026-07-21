import pytest
from app import create_app
from app.models import db

@pytest.fixture
def app():
    app = create_app('../tests/env_test.py')
    return app

@pytest.fixture(autouse=True)
def setup_database(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
