from flask import abort,make_response
from app.models.book import Book
from ..db import db

# database_backed model validation
def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        response = {"message": f"book {book_id} invalid"}
        abort(make_response(response , 400))

    query = db.select(Book).where(Book.id == book_id)
    book = db.session.scalar(query)
    
    if not book:
        response = {"message": f"book {book_id} not found"}
        abort(make_response(response, 404))

    return book


# Option 3: (Hardcode) Refactoring and validating in a helper file
# def validate_book(book_id):
#     try:
#         book_id = int(book_id)
#     except:
#         response = {"message": f"book {book_id} invalid"}
#         abort(make_response(response, 400))

#     for book in books:
#         if book.id == book_id:
#             return book

#     response = {"message": f"book {book_id} not found"}
#     abort(make_response(response, 404))