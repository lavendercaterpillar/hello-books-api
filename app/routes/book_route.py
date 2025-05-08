from flask import Blueprint, Response, abort, make_response, request  
from app.models.book import Book
from ..db import db
from .helper import validate_model


bp = Blueprint("books_bp", __name__, url_prefix="/books") 

# POST request to /books
@bp.post("")
def create_book():
    request_body = request.get_json()  
    
    new_book = Book.from_dict(request_body)

    db.session.add(new_book) 
    db.session.commit() 

    # We need to convert response body back to JSON
    response = new_book.to_dict()
    return response, 201


# GET request with query params
@bp.get("")
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
        books_response.append(book.to_dict())

    return books_response


# Creating a GET request to retrieve 1 book with Validation
@bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_model(Book, book_id)

    # line to refactor
    return book.to_dict()


# Creating a PUT request
@bp.put("/<book_id>")
def update_book(book_id):
    book = validate_model(Book, book_id)
    request_body = request.get_json()
    
    book.update_from_dict(request_body)

    db.session.commit()

    return Response(status=204, mimetype="application/json")


# Creating a DELETE request
@bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_model(Book, book_id)

    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")