# CS50x-Final-Project

## Inventory Management System

## Introduction

My project is a basic and simple web application for **Inventory Management**. The back-end is written using the Flask framework in Python, Front-end is made with HTML, CSS, Javascript, Bootstrap and some Jquery.
For storing data of the inventory, I have used a SQLite database(more on that in the database section). My project is more focused using this for a bookshop but it can be modified for any inventory.

## Video Demo

Demo Video using this application is uploaded on YouTube.

**Link:** [TODO](https://youtube.com)

## Description

Detailed description of the project is as follow

### Tools and Dependencies

Python Dependencies are given in the requirements.txt file

- Install python and pip (added to path)
- Then run following command

```cmd
pip install -r requirements.txt
```

- This will install all the required dependencies and libraries.

Dependencies for the front-end are as follows

- Bootstrap
- Jquery
- Chart.js (For rendering charts and graphs)

For Database Management you can use

- SQlite CLI
- PhpLiteAdmin
- If you use VSCode then SQLite Viewer is a good option

### Launching the application

To launch a flask application, you need a server. Flask has a built-in server which can be easily run using a terminal

But before that we need to configure the some settings of flask to work properly. For that purpose use the following commands while in the project directory

On windows

```cmd
SET FLASK_APP=application.py
SET FLASK_ENV=development
```

On Linux

```bash
export FLASK_APP=application.py
export FLASK_ENV=development
```

After using the above commands in the terminal with the project folder, now run

```cmd
flask run
```

This will run the flask applicaion as localhost on your server. Follow the link in the terminal to view the applicaion in your browser.

### Project Structure

A flask (and many other frameworks) use the MVC or Model View Controller structure. So I will explain the structure in that way as well.

#### Controller

Controller are the backend applications mainly responsible for handling the website routes. For my project the main controller application is the python file **_application.py_**. It handles all the routes for the application accordingly which include webpage routes and ajax routes.

Another python files are **_database.py_** which has all the models for Flask-SQlAlchemy corresponding to the tables in the database. Inherited from the base Model obtained from the library.This is continued in the database section for better understanding of the database.

The last python file is **_helpers.py_**. This file holds just 2 functions. First is the login_required() function which is used as decorator in application.py for those routes which require user to be logged in. And the second is tuple_to_dict() which takes in a tuple with column names and returns a dict. The purpose of this function is to make the tuples returned by queries JSON serializable.

#### Model

Model is basically all the means of data. In my application the model is the SQLite Database **_inventory.db_**.

There are a total of 7 tables in the database.

The first table is the users table which holds the username and password hash for the users(basically inventory managers). The id from this table is unique for every user thus is used for sessioning in application.py

The other tables are the core data storing tables for my application. These tables are linked to each other using Primary and Foreign keys.

Firstly, we have the *types* table. This tables is supposed to take all the types of items you will have in a database. After that linked to it is the *categories* table which holds all the categories related to the specific type. Further we have *sub-categories* that have more sub-categories related to the upper categories. In the end of this chain we have 3 further linked tables which are quite similar to each other but differ in functionality. The inventory holds the curent stock of items in it. The sold_product table is the log of all the products sold at what price and quantity. While the added_products is basically the log of all the investments or items bought.

Now we must talk about Flask-SQlAlchemy and database.py when discussing the model.

Since I have used Flask-SQLAlchemy as the main ORM(Object Relational Mapper) for my project. It requires the use of classes that act as mapping to access the tables. Those classes are defined in the database.py file. And those classes are then used to query data from the database used in application. This approach is secure and better than using Raw SQl (which is possible in SQLAlchemy as well).

#### View

View is basically the appearance of the website which uses HTML, CSS , Bootstrap, Javascript and a little bit of JQuery for ajax calls. For Flask all these html files need to to be placed in the templates folder.

Jinja is the template designer which is used to connect front-end to backend to use/display data.

The layout.html is the basic layout made mostly of the side navbar. This is inherited in all other pages.

The view starts with index page that once logged in displays the current inventory in stock. Next we have the add page in which you can add the items bought to the inventory. The special feature about add.html is that it uses ajax calls using Javacript and JQuery for getting only the categories and sub-categories that correspond to their upper hierarchy. next up is sale.html which is used to record sale of any existing item. This also uses ajax for setting the maximum amount of units that can be sold. Finally we have the reports page which shows all the sold/bought items log and also yearly sales/investments and net loss/profit in the form of graphs.

The static folder holds the styles.css file for styling the webpages as well as all the javascript files for the webpages(mostly for the ajax calls)

## Ending

This is the end of my project. It is a really small scale project with lots of room for improvement and bug fixes. But it was a step towards developing even greater projects in the coming future.

THIS WAS CS50x
