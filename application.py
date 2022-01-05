# Importing libraries and custom classes/functions
from flask import Flask, redirect, request, render_template, session, jsonify, flash
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import generate_password_hash, check_password_hash
from tempfile import mkdtemp
from sqlalchemy.orm import load_only
from database import db, User, Type, Category, Sub_Category, Add_Product, Sale_Product, Inventory
from sqlalchemy import text
from helpers import login_required

# Creating and configuring flask app
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Confirguring Database setting
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
# For Linux, below statement will work
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)
db.create_all()

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
# Main Dashboard with the current inventory
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        return redirect("/")

# Register new user/manager
@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "GET":
        return render_template("register.html", error=error)
    else:
        # Checking username
        user_name = request.form.get("username")
        if not user_name:
            error = "Username cannot be empty"
            return render_template("register.html", error=error)
        present_user = User.query.filter_by(username = user_name).first()
        if present_user != None:
            error = "Username not found"
            return render_template("register.html", error=error)

        # Checking password
        password = request.form.get("password")
        if not password:
            error = "Password cannot be empty"
            return render_template("register.html", error=error)
        confirmation = request.form.get("confirmation")
        if not confirmation:
            error = "Confirmation password cannot be empty"
            return render_template("register.html", error=error)
        if password != confirmation:
            error = "Passwords do not match"
            return render_template("register.html", error=error)
        password_hash = generate_password_hash(password)
        # Store in database
        new_user = User(username = user_name, hash = password_hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")


# Logging in a registered user
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    error = None
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        user_name = request.form.get("username")
        if not user_name:
            error = "Username cannot be empty"
            return render_template("login.html", error=error)
        password = request.form.get("password")
        if not password:
            error = "Password canno be empty"
            return render_template("login.html", error=error)
        rows = User.query.filter_by(username = user_name).first()
        if rows == None or not check_password_hash(rows.hash, password):
            error = "Incorrect username or password"
            return render_template("login.html", error=error)
        session["user_id"] = rows.id
        return redirect("/")
    else:
        return render_template("login.html", error=error)


# Logout a user and clear its session
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# Add an Item to the inventory
@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    error = None
    if request.method == "GET":
        types = Type.query.options(load_only(Type.id, Type.type)).all()
        categories = Category.query.options(load_only(Category.id, Category.category)).all()
        sub_categories = Sub_Category.query.options(load_only(Sub_Category.id, Sub_Category.sub_category)).all()
        return render_template("add.html", types=types, categories=categories, sub_categories=sub_categories, error=error)
    else:
        error  = None
        type_id = request.form.get('type_selection')
        category_id = request.form.get('category_selector')
        sub_category_id = request.form.get('sub_category_selector')
        name = request.form.get("item_name")
        quantity = request.form.get("item_quantity")
        price = request.form.get("item_cost")
        if not type_id:
            error = "Type not selected"
        elif not category_id:
            error = "Category not selected"
        elif not sub_category_id:
            error = "Sub-Category not selected"
        elif not name:
            error = "Item's name not entered"
        elif not quantity:
            error = "Quantity not entered"
        elif not price:
            error = "Price not entered"
        else:
            product_to_add = Add_Product(name = name, quantity = quantity, price=price, sub_category_id=sub_category_id)
            db.session.add(product_to_add)
            if Inventory.query.filter_by(name = name).count() == 0:
                product = Inventory(name = name, quantity = quantity, price = price, sub_category_id = sub_category_id, old = True)
                db.session.add(product)
                db.session.commit()
            else:
                old_data = Inventory.query.with_entities(Inventory.price, Inventory.quantity).filter_by(name = name).filter(Inventory.old == True).first()
                old_price = old_data[0]
                old_quantity = old_data[1]
                if old_price != price:
                    product = Inventory(name = name, quantity = quantity, price = price, sub_category_id = sub_category_id)
                    db.session.add(product)
                    db.session.commit()
                else:
                    old_data.quantity  = quantity + old_quantity
                    db.session.commit()
            return redirect("/")
        return redirect("/add")


# Add sale log and remove item from Inventory
@app.route("/sale", methods=["GET", "POST"])
@login_required
def sale():
    if request.method == "GET":
        return render_template("sale.html")
    else:
        redirect("/sale")


# Error and exception handling
def errorhandler(e):
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("apology.html", error_name=e.name, error_code=e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)