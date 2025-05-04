from flask import abort,make_response
from app.models.book import Book
from ..db import db

# Refactoring validate_book() to include any input model
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"message": f"model {model_id} invalid"}
        abort(make_response(response , 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)
    
    if not model:
        response = {"message": f"model {model_id} not found"}
        abort(make_response(response, 404))

    return model

