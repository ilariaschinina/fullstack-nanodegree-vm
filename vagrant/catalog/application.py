import json
import random, string
import requests
import httplib2

from flask import Flask, render_template, request, redirect,jsonify, url_for, flash, make_response
from flask import session as login_session
app = Flask(__name__)

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///catalogapp.db"
db = SQLAlchemy(app)

CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']

print(CLIENT_ID)

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, scoped_session
# from db_setup import Category, Item, User

#Creating session and connect to DB
# engine = create_engine('sqlite:///catalogapp.db')
# Base.metadata.bind = engine
# DBSession = scoped_session(sessionmaker(bind=engine))
# session = DBSession()

# from sqlalchemy.orm import relationship
# from sqlalchemy import create_engine

class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    token = Column(String(500), nullable=True)

class Category(db.Model):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = db.relationship(User)

class Item(db.Model):
    __tablename__ = 'item'
    id = Column(Integer, primary_key = True)
    title = Column(String(80), nullable = False)
    author = Column(String(80), nullable = False)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = db.relationship(Category)

	#serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
    #Returns object data in easily serializeable format
        return {
           'name'         : self.name,
           'description'         : self.description,
           'id'         : self.id,
       }


session = db.session

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

@app.route("/login")
def showLogin():
    categories = session.query(Category).all()
    items = session.query(Item).all()
    state = ''.join(random.choice(string.ascii_uppercase+string.digits)
            for x in range(32))
    login_session['state'] = state
    return render_template("login.html", categories = categories, items = items, state = state)

@app.route("/category/<int:category_id>/list")
def showCategory(category_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(Item).filter_by(category_id = category_id).all()
    return render_template("list.html", categories = categories, category = category, items = items)

@app.route('/gconnect', methods = ['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state ID'), 401)
        response.headers['Content-type'] = 'application/json'
        return response
    code = request.data.decode()
    print(code)
    # Upgrade the authorization code into a credentials object
    oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
    oauth_flow.redirect_uri = 'http://localhost:5000/oauth2callback'
    credentials = oauth_flow.step2_exchange(code)
    response = make_response(
        json.dumps('Failed to upgrade the authorization code.'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s') % access_token
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route("/category/<int:category_id>/list/new_item", methods = ['GET','POST'])
def newListItem(category_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id = category_id).one()
    item = Item()
    if 'username' not in login_session:
        return redirect('login')
    if request.method == 'POST':
        print(request.form)
        if request.form['title']:
            item.title = request.form['title']
        if request.form['author']:
            item.author = request.form['author']
        if request.form['description']:
            item.description = request.form['description']
        flash('"%s" has been successfully added' % item.title)
        session.add(item)
        session.commit()
        return render_template("item.html", categories = categories, category = category, item = item)
    else:
        return render_template("newItem.html", categories = categories, category = category, item = item)
    #auth required

@app.route("/category/<int:category_id>/list/<int:item_id>/edit", methods = ['GET','POST'])
def editListItem(category_id, item_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id = category_id).one()
    item = session.query(Item).filter_by(id = item_id).one()
    if 'username' not in login_session:
        return redirect('login')
    if request.method == 'POST':
        print(request.form)
        if request.form['title']:
            item.title = request.form['title']
        if request.form['author']:
            item.author = request.form['author']
        if request.form['description']:
            item.description = request.form['description']
        flash('"%s" has been successfully updated' % item.title)
        session.add(item)
        session.commit()
        return render_template("item.html", categories = categories, category = category, item = item)
    else:
        return render_template("editItem.html", categories = categories, category = category, item = item)
    #auth required

@app.route("/category/<int:category_id>/list/<int:item_id>/delete", methods = ['GET','POST'])
def deleteListItem(category_id, item_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id = category_id).one()
    item = session.query(Item).filter_by(id = item_id).one()
    if 'username' not in login_session:
        return redirect('login')
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('"%s" has been successfully deleted' % item.title)
        return redirect(url_for('showCategory', category_id = category_id))
    else:
        return render_template("deleteItem.html", categories = categories, category = category, item = item)
    #auth required

@app.route("/category/<int:category_id>/list/<int:item_id>")
def showListItems(category_id, item_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id = category_id).one()
    item = session.query(Item).filter_by(id = item_id).one()
    return render_template("item.html", categories = categories, category = category, item = item)
    #show delete edit links if user is logged in

@app.route("/unauthorized")
def unauthorized():
    categories = session.query(Category).all()
    return render_template("unauthorized.html", categories = categories)


if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.run(debug=True, host='0.0.0.0')