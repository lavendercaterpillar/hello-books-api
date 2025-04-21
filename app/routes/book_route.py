'''
    Import the Blueprint class from Flask
    Import the books list (data from our "database") from book.py
    Create an instance of Blueprint for our routes related to the Book model
    Register our blueprint with our app
    Write a route to get all the book records from our "database"
'''
from flask import Blueprint
from app.models.book import books

books_bp = Blueprint("books", __name__)
# books_bp = Blueprint("books_bp", __name__, url_prefix="/books") # I can specify an endpoint as URL_Prefix

@books_bp.get("/books")  # if I have specified endpoint on line 12 then no need for /books here
# @books_bp.get("")
def get_books():
    books_response = []

    for book in books:
        books_response.append(
            {
                "id": book.id,
                "title": book.title,
                "description": book.description
            })
        # books_response.append(dict(   # Another way to define a dict
        #     id = book.id,
        #     title = book.title,
        #     description = book.description
        # ))
    
    return books_response