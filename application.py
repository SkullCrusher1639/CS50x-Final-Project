# Importing libraries and custom classes/functions
from flask import Flask, redirect, request, render_template, session, jsonify, flash
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import generate_password_hash, check_password_hash
from tempfile import mkdtemp
from sqlalchemy import func
from sqlalchemy.orm import load_only
from sqlalchemy.sql import extract
from database import db, User, Type, Category, Sub_Category, Add_Product, Sale_Product, Inventory, sub_categories_link
from helpers import login_required, tuple_to_dict

# Creating and configuring flask app
app = Flask(__name__)
app.secret_key = "hammad"
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


# Configuring jinja
app.jinja_env.add_extension('jinja2.ext.do')

# App routes

# Register new user/manager
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
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
        flash("Successfully Registered. You can now log in using your credentials")
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
        flash("Successfully Logged In")
        return redirect("/")
    else:
        return render_template("login.html", error=error)


# Main Dashboard with the current inventory
@app.route("/")
@login_required
def index():
    product_quantites = Inventory.query.with_entities(Inventory.name, func.sum(Inventory.quantity)) \
                            .group_by(Inventory.name).all()
    product_hierarchy = db.session.query(Inventory.name, Type.type, Category.category, 
                            Sub_Category.sub_category) \
                            .select_from(Inventory)\
                            .join(Sub_Category) \
                            .join(sub_categories_link) \
                            .join(Category) \
                            .join(Type) \
                            .distinct()\
                            .group_by(Inventory.name).all() 
    return render_template("index.html", product_quantites=product_quantites, product_hierarchy=product_hierarchy)


# Add an Item to the inventory
@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    error = None
    if request.method == "GET":
        types = Type.query.options(load_only(Type.id, Type.type)).all()
        return render_template("add.html", types=types)
    else:
        error  = None
        type_id = request.form.get('type_selector')
        category_id = request.form.get('category_selector')
        sub_category_id = request.form.get('sub_category_selector')
        name = request.form.get("item_name")
        quantity = int(request.form.get("item_quantity"))
        price = int(request.form.get("item_cost"))
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
            adding_product = Add_Product(name = name, quantity = quantity, price = price, sub_category_id = sub_category_id)
            db.session.add(adding_product)
            db.session.commit()
            if Inventory.query.filter_by(name = name).count() == 0:
                product = Inventory(name = name, quantity = quantity, price = price, sub_category_id = sub_category_id, old = True)
                db.session.add(product)
                db.session.commit()
            else:
                old_data = Inventory.query.options(load_only(Inventory.id, Inventory.quantity)).filter_by(name = name).filter(Inventory.old == True).first()
                old_price = old_data.price
                old_quantity = old_data.quantity
                if old_price != price:
                    product = Inventory(name = name, quantity = quantity, price = price, sub_category_id = sub_category_id)
                    db.session.add(product)
                    db.session.commit()
                else:
                    old_data.quantity  = quantity + old_quantity
                    db.session.commit()
            flash("Item Added to Inventory")
            return redirect("/")
        types = Type.query.options(load_only(Type.id, Type.type)).all()
        return render_template("add.html", error=error)

# Routes for the ajaz call by add.html
@app.route("/type")
@login_required
def get_categories():
    type = int(request.args.get("q"))
    if type:
        categories = Category.query.with_entities(Category.id, Category.category).join(Type) \
                        .filter(Type.id == type).all()
        if categories != None:
            categories = tuple_to_dict(categories, "id", "category")
    else:
        categories = []
    return jsonify(categories)

@app.route("/cat")
@login_required
def get_sub_categories():
    cat_id = int(request.args.get("q"))
    if cat_id:
        sub_categories = Sub_Category.query.with_entities(Sub_Category.id, Sub_Category.sub_category).\
                            join(sub_categories_link).\
                            join(Category) \
                        .filter(Category.id == cat_id).all()
        if sub_categories != None:
            sub_categories = tuple_to_dict(sub_categories, "id", "sub_category")
    else:
        sub_categories = []
    return jsonify(sub_categories)


# Add sale log and remove item from Inventory
@app.route("/sale", methods=["GET", "POST"])
@login_required
def sale():
    error = None
    if request.method == "GET":
        products = Inventory.query.options(load_only(Inventory.name)).group_by(Inventory.name).filter(Inventory.quantity != 0).all()
        return render_template("sale.html", products=products, error=error)
    else:
        products = Inventory.query.options(load_only(Inventory.name)).group_by(Inventory.name).all()
        name = request.form.get("selected_item")
        quantity = request.form.get("item_quantity")
        price = request.form.get("item_sale")
        if not name:
            error = "Item name not selected"
        elif not quantity:
            error = "Quantity not specified"
            quantity = int(quantity)
        elif not price:
            error = "Price not specified"
            price = int(price)    
        else:
            inventory_data = Inventory.query.filter_by(name = name).filter_by(old = True).first()
            sold_product = Sale_Product(name = name, quantity = quantity, price = price, sub_category_id = inventory_data.sub_category_id)
            db.session.add(sold_product)
            inventory_data.quantity = inventory_data.quantity - int(quantity)
            db.session.commit()
            flash("Item sold")
            return redirect("/")
        products = Inventory.query.options(load_only(Inventory.name)).group_by(Inventory.name).filter(Inventory.quantity != 0).all() 
        return render_template("sale.html", products=products, error=error)

# Route for the ajax call used in sale.html
@app.route("/quantity")
@login_required
def get_quantity():
    name = request.args.get("q")
    if name:
        quantity_obj = Inventory.query.with_entities(Inventory.quantity).filter_by(name = name)
        if quantity_obj.count() == 0:
            return redirect("/sale")
        else:
            quantity_obj = quantity_obj.filter_by(old = True).first()
            if quantity_obj is None or quantity_obj[0] == 0:
                quantity_obj = Inventory.query.options(load_only(Inventory.quantity, Inventory.old)).filter_by(name = name).first()
                quantity_obj.old = True
                db.session.commit()
                quantity = quantity_obj.quantity
            else:
                quantity = quantity_obj[0]
    else:
        quantity = 0
    quantity_required = {"quantity" : quantity}
    return jsonify(quantity_required)


# Route for the reports page
@app.route("/reports")
@login_required
def reports():
    added_product_log = Add_Product.query.with_entities(Add_Product.name, Add_Product.price, 
                            Add_Product.quantity, Add_Product.date)
    sold_product_log = Sale_Product.query.with_entities(Sale_Product.name, Sale_Product.price, 
                            (Sale_Product.quantity) * -1, Sale_Product.date)
    complete_log = (sold_product_log.union_all(added_product_log)).order_by(Add_Product.date) \
                        .order_by(Add_Product.price).all()
    return render_template("report.html", logs=complete_log)

# Route for the ajax call to get monthly data
@app.route("/months")
def get_monthly_data():
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    monthly_data = []
    for i in range(12):
        data_sale = db.session.query(func.sum(Sale_Product.price * Sale_Product.quantity)).\
            filter(extract("month", Sale_Product.date) == (i + 1)).first()
        data_add = db.session.query(func.sum(Add_Product.price * Add_Product.quantity)). \
            filter(extract("month", Add_Product.date) == (i + 1)).first()
        if data_sale[0]:
            data_month_sale = data_sale[0]
        else:
            data_month_sale = 0
        if data_add[0]:
            data_month_add = data_add[0]
        else:
            data_month_add = 0
        monthly_data.append({"month" : months[i], "sale": data_month_sale , "add": data_month_add,
                                 "net": data_month_sale - data_month_add})
    return jsonify(monthly_data)

# Logout a user and clear its session
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")



# Error and exception handling
def errorhandler(e):
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("apology.html", error_name=e.name, error_code=e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)