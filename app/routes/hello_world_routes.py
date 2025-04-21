from flask import Blueprint

#defining Blueprint
hello_world_bp = Blueprint("hello_world", __name__)

#defining endpoint
@hello_world_bp.get("/")
def say_hello_world():
    return "Hello, World!"