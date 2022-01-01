# Importing libraries and custom classes/functions
from flask import Flask, redirect, request, render_template, session, jsonify, flash
from database import db

# Creating and configuring flask app and SQLALchemy
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
# For Linux below statement will work
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)


# App routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", session=None)
    else:
        return redirect("/")