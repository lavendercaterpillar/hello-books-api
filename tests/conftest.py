import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.models.book import Book
from app.models.author import Author


#Before we can use our environment variables, we need to invoke the load_dotenv function that we imported.
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


@pytest.fixture
def two_saved_books(app): # This fixture needs to request the use of the app fixture above, so we know the test database has been initialized.
    # Arrange
    ocean_book = Book(title="Ocean Book",
                        description="watr 4evr")
    mountain_book = Book(title="Mountain Book",
                        description="i luv 2 climb rocks")

    db.session.add_all([ocean_book, mountain_book])  # to add a list of instances
    # Alternatively, we could do
    # db.session.add(ocean_book)
    # db.session.add(mountain_book)
    db.session.commit()  # commits and saves our books to the database


@pytest.fixture
def two_saved_authors(app): 
    # Arrange
    ocean_author = Author(title="Ocean author")
    mountain_author = Author(title="Mountain author")

    db.session.add_all([ocean_author, mountain_author]) 
    # Alternatively, we could do
    # db.session.add(ocean_author)
    # db.session.add(mountain_author)
    db.session.commit() 

