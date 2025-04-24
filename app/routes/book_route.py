from flask import Blueprint, abort, make_response, request  # additional imports for refactoring option 2
from app.models.book import Book
from ..db import db

# books_bp = Blueprint("books_bp", __name__)
books_bp = Blueprint("books_bp", __name__, url_prefix="/books") 


# Creating a POST request
@books_bp.post("")
def create_book():
    request_body = request.get_json()  # JSON is a string, needs to convert it back into python data types
    title = request_body["title"]
    description = request_body["description"]

    new_book = Book(title=title, description=description)
    db.session.add(new_book)
    db.session.commit()

    # We need to convert response back to JSON
    response = {
        "id": new_book.id,
        "title": new_book.title,
        "description": new_book.description,
    }
    return response, 201