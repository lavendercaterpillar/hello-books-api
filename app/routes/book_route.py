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
    # query = db.select(Book) # similar to SELECT in SQL
    query = db.select(Book).order_by(Book.id)  # sorted in a particular order by calling order_by  
    books = db.session.scalars(query) # This method returns the query which is a list of instances of Book.

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


# # Creating a GET request to retrieve 1 book
# @books_bp.get("/<book_id>")  # Place holder for book_id endpoint in the GET request
# def get_one_book(book_id):
#     # Similar to SELECT <> WHERE <> in SQL
#     query = db.select(Book).where(Book.id == book_id)
#     book = db.session.scalar(query) # returns based on the above query (book_id)

#     return {
#         "id": book.id,
#         "title": book.title,
#         "description": book.description
#     }


# Creating a GET request to retrieve 1 book with Validation
@books_bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_book(book_id)

    return {
        "id": book.id,
        "title": book.title,
        "description": book.description,
    }


# Creatign a PUT request
@books_bp.put("/<book_id>")
def update_book(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")