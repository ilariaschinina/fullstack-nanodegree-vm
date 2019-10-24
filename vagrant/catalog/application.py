import json
from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from db_setup import Base, Category, Item, User

#Creating session and connect to DB
engine = create_engine('sqlite:///catalogapp.db')
Base.metadata.bind = engine
DBSession = scoped_session(sessionmaker(bind=engine))
session = DBSession()

#Fake Categories
# category = {'name': 'Dogs', 'id': '1'}
# categories = [{'name': 'Dogs', 'id': '1'}, {'name':'Cats', 'id':'2'},{'name':'Raccoons', 'id':'3'}]


# #Fake List Items
# item = {'name':'Husky', 'description':'good boi', 'id': '1'}
# items = [ {'name':'Husky', 'description':'good boi', 'id': '1'}, {'name':'Bernese','description':'very good boi', 'id':'2'},{'name':'German boi', 'description':'extremely good boi','id':'3'}]


# category1 = Category(name = "Python", user = user1)
# item1 = Item(title = "", author= "", description = "", category = category1)

@app.route("/")
def home():
    categories = session.query(Category).all()
    #TODO: filter latest items
    items = session.query(Item).all()
    return render_template("home.html", categories = categories, items = items)

# @app.route("/category/new")
# def newCategory():
#     return "This is to create a new category"
#     #auth required

# @app.route("/category/<int:category_id>/edit")
# def editCategory(category_id):
#     return "This is to update this category"
#      #auth required

# @app.route("/category/<int:category_id>/delete")
# def deleteCategory(category_id):
#     return "This is to delete this category"
#      #auth required

@app.route("/category/<int:category_id>/list")
def showCategory(category_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(Item).filter_by(category_id = category_id).all()
    return render_template("list.html", categories = categories, category = category, items = items)

@app.route("/category/<int:category_id>/list/new_item")
def newListItem(category_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id = category_id).one()
    return render_template("newItem.html", categories = categories, category = category)
    #auth required

@app.route("/category/<int:category_id>/list/<int:item_id>/edit")
def editListItem(category_id, item_id):
    categories = session.query(Category).all()
    item = session.query(Item).filter_by(id = item_id).one()
    return render_template("editItem.html", categories = categories, item = item)
    #auth required

@app.route("/category/<int:category_id>/list/<int:item_id>/delete")
def deleteListItem(category_id, item_id):
    categories = session.query(Category).all()
    item = session.query(Item).filter_by(id = item_id).one()
    return render_template("deleteItem.html", categories = categories, item = item)
    #auth required

@app.route("/category/<int:category_id>/list/<int:item_id>")
def showListItems(category_id, item_id):
    categories = session.query(Category).all()
    item = session.query(Item).filter_by(id = item_id).one()
    return render_template("item.html", categories = categories, item = item)
    #show delete edit links if user is logged in

@app.route("/unauthorized")
def unauthorized():
    categories = session.query(Category).all()
    return render_template("unauthorized.html", categories = categories)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')