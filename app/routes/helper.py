from flask import abort,make_response
from app.models.book import books


## Option 3: Refactoring and validating in a helper file
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