from flask import Blueprint, Response, abort, make_response, request
from app.models.author import Author
from ..db import db
from .helper import validate_model

bp = Blueprint("authors_bp", __name__, url_prefix="/authors")

# POST endpoint
@bp.post("")
def create_author():
    request_body = request.get_json()
    
    try:
        new_author = Author.from_dict(request_body)
        
    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))


    db.session.add(new_author) 
    db.session.commit() 

    response = new_author.to_dict()
    return response, 201


# Due to one to many relationship we can
# read a list of books related to one author (Parent model)
# GET All Books from an Author
@bp.get("/<author_id>/books")
def get_books_by_author(author_id):
    author = validate_model(Author, author_id)
    response = [book.to_dict() for book in author.books]
    return response


# Due to "one to many" relationship we can create a book with author:
# POST request by parent model (with list of children models) better to say many to one instead
@bp.post("/<author_id>/book")
def create_book():
    request_body = request.get_json()  
    
    try:
        new_book = Book.from_dict(request_body)
    except KeyError as e:
        response = {"message": f"Invalid request: missing {e.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_book) 
    db.session.commit() 

    # We need to convert response body back to JSON
    response = new_book.to_dict()
    return response, 201



# GET all endpoint
@bp.get("")
def get_all_authors():

    query = db.select(Author)

    name_param = request.args.get("name")
    if name_param:
        query = query.where(Author.name.ilike(f"%{name_param}%"))

    query = query.order_by(Author.id)
    authors = db.session.scalars(query)
    
    authors_response = []
    for author in authors:
            # line to refactor
        authors_response.append(author.to_dict())

    return authors_response


@bp.get("/<author_id>")
def get_one_author(author_id):
    author = validate_model(Author, author_id)

    return author.to_dict()


@bp.put("/<author_id>")
def update_author(author_id):
    author = validate_model(Author, author_id)
    request_body = request.get_json()
    
    author.name = request_body["name"]
    
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<author_id>")
def delete_author(author_id):
    author = validate_model(Author, author_id)
    db.session.delete(author)
    db.session.commit()

    return Response(status=204, mimetype="application/json")