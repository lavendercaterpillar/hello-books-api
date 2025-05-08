from flask import Flask
from .db import db, migrate
from .models import book, author
from .routes.book_route import bp as books_bp
from .routes.author_route import bp as authors_bp
import os

def create_app(config=None):  # None, making the parameter optional
    app = Flask(__name__)

    # SQLAlchemy settings

    # Hide a warning
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        # Merge `config` into the app's configuration
        # to override the app's default settings
        app.config.update(config)


    # Registering DB and migrate here
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    app.register_blueprint(books_bp)
    app.register_blueprint(authors_bp)

    return app