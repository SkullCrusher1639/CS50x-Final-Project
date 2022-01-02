# Importing libraries and custom classes/functions
from flask import Flask, redirect, request, render_template, session, jsonify, flash
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import generate_password_hash, check_password_hash
from tempfile import mkdtemp
from database import db

# Creating and configuring flask app
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Confirguring Database setting
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
# For Linux below statement will work
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)

# Configuring session/cookies settings
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# App routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", session=None)
    else:
        return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "GET":
        return render_template("register.html", error=error)
    else:
        # Checking username
        user_name = request.form.get("username")
        if not user_name:
            error = True
            return render_template("register.html", error=error)
        #count = db.execute('SELECT username FROM users WHERE username = ?', user_name)
        #if len(count) != 0:
         #   error = True
          #  return render_template("register.html", error=error)

        # Checking password
        password = request.form.get("password")
        if not password:
            error = True
            return render_template("register.html", error=error)
        confirmation = request.form.get("confirmation")
        if not confirmation:
            error = True
            return render_template("register.html", error=error)
        if password != confirmation:
            error = True
            return render_template("register.html", error=error)
        password_hash = generate_password_hash(password)
        #Store in database
        #db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", user_name, password_hash)
        return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    error = None
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            error = True
            return render_template("login.html", error=error)
        elif not request.form.get("password"):
            error = True
            return render_template("login.html", error=error)
        #rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        #if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
        #    error = True
        #    return render_template("login.html", error=error)

        #session["user_id"] = rows[0]["id"]
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", error=error)


# Error and exception handling
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("apology.html", error_name=e.name, error_code=e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)