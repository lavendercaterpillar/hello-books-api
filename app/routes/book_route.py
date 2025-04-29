from flask import Blueprint, Response, request  # additional imports for refactoring option 2
from app.models.book import Book
from ..db import db
from .helper import validate_book

# books_bp = Blueprint("books_bp", __name__)
books_bp = Blueprint("books_bp", __name__, url_prefix="/books") 


# Creating a POST request
@books_bp.post("")
def create_book():
    request_body = request.get_json()  # JSON is a string, needs to convert it back into python data types
    title = request_body["title"]
    description = request_body["description"]

    new_book = Book(title=title, description=description)

    # lines 18 and 19 are responsible for saving the new book to the database.
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

    title_param = request.args.get("title") # this will look up the query params "title" using request.args
    if title_param:
        ## code that builds a query to filter by "title":exact match
        # query = db.select(Book).where(Book.title == title_param).order_by(Book.id)
        # code that filter partial string "title":partial match
        query = db.select(Book).where(Book.title.ilike(f"%{title_param}%")).order_by(Book.id)
    else:
        query = db.select(Book).order_by(Book.id)

    books = db.session.scalars(query) 

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


# Creating a GET request to retrieve 1 book with Validation
@books_bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_book(book_id)

    return {
        "id": book.id,
        "title": book.title,
        "description": book.description,
    }


# Creating a PUT request
@books_bp.put("/<book_id>")
def update_book(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")


# Creatign a DELETE request
@books_bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_book(book_id)
    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")