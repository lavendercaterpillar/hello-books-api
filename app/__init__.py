from flask import Flask
from .routes.book_route import books_bp

def create_app():
    app = Flask(__name__)

    # Registering Blueprints here
    # app.register_blueprint(hello_world_bp)
    app.register_blueprint(books_bp)

    return app