from flask_sqlalchemy import SQLAlchemy
from datetime import date
db=SQLAlchemy()

# User Table for BookShop Managers
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable = False)
    hash = db.Column(db.Text, nullable = False)


# Tables for Inventory data

# Class which contains all types for the inventory
class Type(db.Model):
    __tablename__ = "types"
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.Text, nullable = False)
    categories = db.relationship("Category", backref="type")



# Association table for categories and sub-categories
sub_categories_link = db.Table('sub_categories_link',
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id')),
    db.Column('sub_category_id', db.Integer, db.ForeignKey('sub_categories.id'))
)

# Class for all the categories related to the types of products
class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.Text, nullable = False)
    type_id = db.Column(db.Integer, db.ForeignKey("types.id"))
    sub_categories = db.relationship("Sub_Category", secondary=sub_categories_link, 
                        backref=db.backref("category", lazy = "dynamic"))

# Class for all the sub-categories related to categories of items
class Sub_Category(db.Model):
    __tablename__ = "sub_categories"
    id = db.Column(db.Integer, primary_key = True)
    sub_category = db.Column(db.Integer, nullable = False)
    add_products = db.relationship("Add_Product", backref="sub_category")

# Class for the Product Add Table
class Add_Product(db.Model):
    __tablename__ = "added_products"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text, nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    cost = db.Column(db.Integer, nullable = False)
    sale = db.Column(db.Integer, nullable = False, default=0)
    date = db.Column(db.Date, nullable = False, default=date.today())
    sub_category_id = db.Column(db.Integer,db.ForeignKey("sub_categories.id"))

# Class for the Products sold Table
class Sale_Product(db.Model):
    __tablename__ = "sold_products"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text, nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    cost = db.Column(db.Integer, nullable = False, default = 0)
    sale = db.Column(db.Integer, nullable = False)
    date = db.Column(db.Date, nullable = False, default=date.today())
    sub_category_id = db.Column(db.Integer,db.ForeignKey("sub_categories.id"))