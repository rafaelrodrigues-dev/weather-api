import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app

@pytest.fixture
def client():
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
