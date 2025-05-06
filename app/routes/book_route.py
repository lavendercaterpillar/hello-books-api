from flask import Blueprint, Response, make_response, request  # additional imports for refactoring option 2
from app.models.book import Book
from ..db import db
from .helper import validate_model

# books_bp = Blueprint("books_bp", __name__)
books_bp = Blueprint("books_bp", __name__, url_prefix="/books") 


# Creating a POST request
@books_bp.post("")
def create_book():
    request_body = request.get_json()  # JSON is a string, needs to convert it back into python data types
    
    # lines to raftrefactor
    # title = request_body["title"]
    # description = request_body["description"]
    # new_book = Book(title=title, description=description)

    new_book = Book.from_dict(request_body)

    # lines 18 and 19 are responsible for saving the new book to the database.
    db.session.add(new_book) 
    db.session.commit() 

    # We need to convert response body back to JSON
    response = new_book.to_dict()
    return response, 201


# Creating a GET request with query params
@books_bp.get("")
def get_all_books():

    query = db.select(Book)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Book.title.ilike(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Book.description.ilike(f"%{description_param}%"))

    # query = query.order_by(Book.id)
    # books = db.session.scalars(query)
    books = db.session.scalars(query.order_by(Book.id))
    
    books_response = []
    for book in books:
            # line to refactor
        books_response.append(book.to_dict())

    return books_response

# # Creating a GET all BROKEN for test
# @books_bp.get("")
# def get_all_books():
#     return make_response("I'm a teapot!", 418)


# Creating a GET request to retrieve 1 book with Validation
@books_bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_model(Book, book_id)

    # line to refactor
    return book.to_dict()


# Creating a PUT request
@books_bp.put("/<book_id>")
def update_book(book_id):
    book = validate_model(Book, book_id)
    request_body = request.get_json()
    
    # book.title = request_body["title"]
    # book.description = request_body["description"]
    
    # Two lines above can be replaced with a instance method
    book.update_from_dict(request_body)

    db.session.commit()

    return Response(status=204, mimetype="application/json")


# Creatign a DELETE request
@books_bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_model(Book, book_id)
    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")