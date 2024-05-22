from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user_model import User

def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if user and user.role == role:
                return fn(*args, **kwargs)
            else:
                return jsonify({"msg": "Unauthorized"}), 403
        return decorator
    return wrapper
