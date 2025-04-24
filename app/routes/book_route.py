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

    # lines 18 and 19 are responsible for saving a new book to the database.
    db.session.add(new_book) # Think of it like staging the object—it's marked to be inserted into the database, but it’s not saved yet.
    db.session.commit() # At this point, the new_book is inserted into the database, and if your Book model has an auto-incrementing ID, it gets assigned right here.

    # We need to convert response body back to JSON
    response = {
        "id": new_book.id,
        "title": new_book.title,
        "description": new_book.description,
    }
    return response, 201


# Creating a GET request for retrieving ALL books
@books_bp.get("")
def get_all_books():
    # query = db.select(Book) # similar to SELECT in SQL
    query = db.select(Book).order_by(Book.id)  # sorted in a particular order by calling order_by  
    books = db.session.scalars(query) # This method returns a list of instances of Book.

    # We could also write the lines above as:
    # books = db.session.execute(query).scalars()

    books_response = []
    for book in books:
        books_response.append(
            {
                "id": book.id,
                "title": book.title,
                "description": book.description
            }
        )
    return books_response