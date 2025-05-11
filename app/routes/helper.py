from flask import abort,make_response
from ..db import db

# Refactoring validate_book() to include any input model
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"message": f"{cls.__name__} {model_id} invalid"}
        abort(make_response(response , 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)
    
    if not model:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))

    return model

# we can also create the follwoing function to reduce the size of our route fucntions.
# Creates a dictionary form of a Class instance from a request body
# and return JSON of the dict and status code

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
        
    except KeyError as error:
        # response = {"message": f"Invalid request: missing {error.args[0]}"}
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201