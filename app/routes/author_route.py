from flask import Blueprint, Response, make_response, request
from app.models.author import Author
from ..db import db
from .helper import validate_model

authors_bp = Blueprint("authors_bp", __name__, url_prefix="/authors")

# POST endpoint
@authors_bp.post("")
def create_author():
    request_body = request.get_json()
    new_author = Author.from_dict(request_body)

    db.session.add(new_author) 
    db.session.commit() 

    response = new_author.to_dict()
    return response, 201


# GET all endpoint
@authors_bp.get("")
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


@authors_bp.get("/<author_id>")
def get_one_author(author_id):
    author = validate_model(Author, author_id)

    return author.to_dict()


@authors_bp.put("/<author_id>")
def update_author(author_id):
    author = validate_model(Author, author_id)
    request_body = request.get_json()
    
    author.name = request_body["name"]
    
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@authors_bp.delete("/<author_id>")
def delete_author(author_id):
    author = validate_model(Author, author_id)
    db.session.delete(author)
    db.session.commit()

    return Response(status=204, mimetype="application/json")