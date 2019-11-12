import json
import random
import string

from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash, make_response
from flask import session as login_session

# Requests + OAuth stuff
from oauthlib.oauth2 import WebApplicationClient
import requests
from requests_oauthlib import OAuth2Session


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import relationship

# Create flask app and set db path
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///catalogapp.db"
db = SQLAlchemy(app)

# Parse client_secret.json file to retrieve credentials for using Google Auth
API_CLIENT_DATA = json.loads(open('client_secret.json', 'r').read())['web']
GOOGLE_CLIENT_ID = API_CLIENT_DATA['client_id']
GOOGLE_CLIENT_SECRET = API_CLIENT_DATA['client_secret']
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Constants for creating OAuth2 objects
authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
token_url = "https://www.googleapis.com/oauth2/v4/token"
scope = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid"
]

session = db.session


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True, index=True)
    picture = Column(String(250), nullable=False)


class Category(db.Model):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Returns object data in easily serializeable format"""
        return {
           'name': self.name,
           'user_id': self.user_id,
           'id': self.id
        }


class Item(db.Model):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    author = Column(String(80), nullable=False)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        """Returns object data in easily serializeable format"""
        category = session.query(Category).filter_by(id=self.category_id).one()
        return {
           'title': self.title,
           'author': self.author,
           'description': self.description,
           'category': category.serialize,
           'id': self.id,
        }

# Routing
@app.route("/")
def home():
    categories = session.query(Category).all()
    items = session.query(Item).order_by(Item.id.desc()).limit(10).all()
    is_logged_in = 'user_id' in login_session
    return render_template("home.html", categories=categories,
                           items=items, is_logged_in=is_logged_in)


@app.route("/login")
def showLogin():
    google = OAuth2Session(GOOGLE_CLIENT_ID, scope=scope,
                           redirect_uri="http://localhost:5000/oauth2callback")
    authorization_url, state = google.authorization_url(
                                                        authorization_base_url,
                                                        access_type="offline",
                                                        prompt="select_account"
                                                        )
    login_session['state'] = state

    return redirect(authorization_url)


@app.route('/oauth2callback', methods=['GET'])
def gconnect():

    google = OAuth2Session(
        GOOGLE_CLIENT_ID, state=login_session['state'], scope=scope,
        redirect_uri="http://localhost:5000/oauth2callback"
        )
    google.fetch_token(
        token_url, client_secret=GOOGLE_CLIENT_SECRET,
        authorization_response=request.url
        )
    userinfo_response = google.get(
                        'https://www.googleapis.com/oauth2/v1/userinfo'
                        )

    """You want to make sure their email is verified.
    The user authenticated with Google, authorized your
    app, and now you've verified their email through Google!"""
    if userinfo_response.json().get("verified_email"):
        login_session['email'] = userinfo_response.json()["email"]
        login_session['picture'] = userinfo_response.json()["picture"]
        login_session['username'] = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    try:
        user = session.query(User).filter_by(
                                    email=login_session['email']).one()

    except NoResultFound:
        user = User(email=login_session['email'])
    user.name = login_session['username']
    user.picture = login_session['picture']

    session.add(user)
    session.commit()

    login_session['user_id'] = user.id

    """Redirect back to the page the user was on if it's known,
    otherwise the home page"""
    return redirect("/")


@app.route('/gdisconnect')
def gdisconnect():
    del login_session['user_id']
    return redirect("/")


@app.route("/category/<int:category_id>/list")
def showCategory(category_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    is_logged_in = 'user_id' in login_session
    is_owner = is_logged_in and login_session['user_id'] == category.user_id

    return render_template(
        "list.html", categories=categories, category=category, items=items,
        is_owner=is_owner, is_logged_in=is_logged_in
        )


@app.route("/category/<int:category_id>/list/new_item",
           methods=['GET', 'POST'])
def newListItem(category_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    is_logged_in = 'user_id' in login_session
    if 'user_id' not in login_session:
        flash('Please, log in in order to add a new item')
        return redirect('/category/%s/list' % (category_id))

    if login_session['user_id'] != category.user_id:
        flash("You are not authorized to add new books to this category")
        return redirect('/category/%s/list' % category_id)

    if request.method == 'POST':
        item = Item()
        if request.form['title']:
            item.title = request.form['title']
        if request.form['author']:
            item.author = request.form['author']
        if request.form['description']:
            item.description = request.form['description']
        flash('"%s" has been successfully added' % item.title)
        session.add(item)
        session.commit()
        return render_template(
            "item.html", categories=categories, category=category, item=item,
            is_owner=True, is_logged_in=is_logged_in
            )
    else:
        return render_template("newItem.html", categories=categories,
                               category=category, is_logged_in=is_logged_in)


@app.route("/category/<int:category_id>/list/<int:item_id>/edit",
           methods=['GET', 'POST'])
def editListItem(category_id, item_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    is_logged_in = 'user_id' in login_session
    if not is_logged_in:
        flash('Please, log in in order to edit')
        return redirect('/category/%s/list/%s' % (category_id, item_id))

    if login_session['user_id'] != category.user_id:
        flash("You are not authorized to edit books to this category")
        return redirect('/category/%s/list/%s' % (category_id, item_id))

    if request.method == 'POST':
        if request.form['title']:
            item.title = request.form['title']
        if request.form['author']:
            item.author = request.form['author']
        if request.form['description']:
            item.description = request.form['description']
        flash('"%s" has been successfully updated' % item.title)
        session.add(item)
        session.commit()
        return render_template(
            "item.html", categories=categories, category=category, item=item,
            is_owner=True, is_logged_in=is_logged_in
            )
    else:
        return render_template(
            "editItem.html", categories=categories, category=category,
            item=item, is_logged_in=is_logged_in
            )


@app.route("/category/<int:category_id>/list/<int:item_id>/delete",
           methods=['GET', 'POST'])
def deleteListItem(category_id, item_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    is_logged_in = 'user_id' in login_session
    if not is_logged_in:
        flash('Please, log in in order to delete')
        return redirect('/category/%s/list/%s' % (category_id, item_id))

    if login_session['user_id'] != category.user_id:
        flash("You are not authorized to delete books to this category")
        return redirect('/category/%s/list/%s' % (category_id, item_id))
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('"%s" has been successfully deleted' % item.title)
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template(
            "deleteItem.html", categories=categories, category=category,
            item=item, is_logged_in=is_logged_in
            )


@app.route("/category/<int:category_id>/list/<int:item_id>")
def showListItems(category_id, item_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    is_logged_in = 'user_id' in login_session
    is_owner = is_logged_in and login_session['user_id'] == category.user_id
    return render_template(
        "item.html", categories=categories, category=category, item=item,
        is_owner=is_owner, is_logged_in=is_logged_in
        )


# JSON API endpoints
@app.route('/category/<int:category_id>/JSON')
def listJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return jsonify(category.serialize)


@app.route('/category/<int:category_id>/list/<int:item_id>/JSON')
def itemJSON(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(item=item.serialize)


@app.route('/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[i.serialize for i in categories])


if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.run(debug=True, host='0.0.0.0')
