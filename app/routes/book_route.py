'''
    Import the Blueprint class from Flask
    Import the books list (data from our "database") from book.py
    Create an instance of Blueprint for our routes related to the Book model
    Register our blueprint with our app
    Write a route to get all the book records from our "database"
'''
from flask import Blueprint, abort, make_response  # additional imports for refactoring
from app.models.book import books

# books_bp = Blueprint("books_bp", __name__)
books_bp = Blueprint("books_bp", __name__, url_prefix="/books") # I can specify an endpoint as URL_Prefix

# @books_bp.get("/books")  # if I have specified endpoint on line 12 then no need for /books here
@books_bp.get("")
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

# second endpoint for one book
@books_bp.get("/<book_id>") # now with this endpoint we need to use line 12 instead of line 11
def get_one_book(book_id):

    ## Option 1: direct Error Handling
    # try:
    #     book_id = int(book_id)
    # except:
    #     return {"message": f"book {book_id} invalid"}, 400 # handling invalid book_id

    # for book in books:
    #     if book.id == book_id:
    #         return {
    #             "id": book.id,
    #             "title": book.title,
    #             "description": book.description,
    #         }
    # return {"message": f"book {book_id} not found"}, 404  # handling not found book_id


    # Option 2: Refactoring
    book = validate_book(book_id)

    return {
        "id": book.id,
        "title": book.title,
        "description": book.description,
    }
    


def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        response = {"message": f"book {book_id} invalid"}
        abort(make_response(response, 400))

    for book in books:
        if book.id == book_id:
            return book

    response = {"message": f"book {book_id} not found"}
    abort(make_response(response, 404))