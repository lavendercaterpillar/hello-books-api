import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os

load_dotenv()

@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config) # passing test Configure;also it merges test configue with app.config (app default config)

    @request_finished.connect_via(app)  # this decorator defines what will be invoked after a request is completed
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all() # At the start of each test, this code recreates the tables needed for our models.
        yield app

    with app.app_context():
        db.drop_all()  # After the test runs, this will drop all of the tables, deleting any data that was created during the test.



@pytest.fixture
def client(app):
    return app.test_client()