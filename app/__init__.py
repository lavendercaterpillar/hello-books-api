from flask import Flask
from .db import db, migrate
from .models import book 
from .routes.book_route import books_bp

def create_app():
    app = Flask(__name__)

    # SQLAlchemy settings
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Hide a warning

    # Set the Connection String; Here we tell Flask where to find the new DB
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_development'

    # Registering DB and migrate here
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Registering Blueprints here
    # app.register_blueprint(hello_world_bp)
    app.register_blueprint(books_bp)

    return app