from flask import redirect, render_template, request, session

def login_required(func):
    def wrapper():
        if session.get("user_id") is None:
            return redirect("/login")
        return func
    return wrapper