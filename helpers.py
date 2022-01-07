from functools import wraps
from flask import redirect, session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def tuple_to_dict(values, key1, key2):
    required = []
    for value in values:
        required.append({key1: value[0] , key2: value[1].capitalize().replace("_", "-")})
    return required