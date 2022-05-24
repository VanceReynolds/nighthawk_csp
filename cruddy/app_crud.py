"""control dependencies to support CRUD app routes and APIs"""
import datetime
from flask import Blueprint, render_template, request, url_for, redirect, jsonify, make_response
from flask_login import login_required, logout_user

from cruddy.query import *

# blueprint defaults https://flask.palletsprojects.com/en/2.0.x/api/#blueprint-objects
app_crud = Blueprint('crud', __name__,
                     url_prefix='/crud',
                     template_folder='templates/cruddy/',
                     static_folder='static',
                     static_url_path='static')

""" Blueprint is established to isolate Application control code for CRUD operations, key features:
    1.) 'Users' table control methods, controls relationship between User Actions and Database Model
    2.) Control methods are achieved using app routes for each CRUD operations
    3.) login required to restrict CRUD operations to identified users
"""


# If you decorate a view(route) with this, it will ensure that the current user is logged in and authenticated before calling the actual view. 
# (If they are not, it calls the LoginManager.unauthorized callback.). 
# Use this example for Hack #3.
@app_crud.route('/')
@login_required  # Flask-Login uses this decorator to restrict acess to logged in users
def crud():
    """obtains all Users from table and loads Admin Form"""
    return render_template("crud.html", table=users_all(), username=str(current_user.name))


# Unauthorised users do not get access to the SQL CRUD
# Flask-Login directs unauthorised users to this unauthorized_handler
@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    return redirect(url_for('crud.crud_login'))

# return currently logged in username or anonymous
def get_login_username():
    if current_user is None or current_user.is_anonymous == True:
        return "anonymous"
    else:
        return str(current_user.name)

# if login url, show phones table only
@app_crud.route('/login/', methods=["GET", "POST"])
def crud_login():
    # if there is a user logged in when we get here, log them out
    if current_user is not None and current_user.is_anonymous == False:
        logout_user()

    # obtains form inputs and fulfills login requirements
    if request.form:
        email = request.form.get("email")
        password = request.form.get("password")
        remember = request.form.get("remember")
        # in order to forget me we must include seconds until we are forgotten
        if (remember is None or remember == False):
            remember_me = False
            duration = datetime.timedelta(seconds=180) 
        # forget us after a day anyway so it is easier to test tomorrow
        else:
            remember_me = True
            duration = datetime.timedelta(days=1)

        # pass in the name of the logged in user so it can be shown
        if login(email, password, remember_me, duration):       # zero index [0] used as email is a tuple
            return redirect(url_for('crud.crud', username=get_login_username()))

    # if not logged in, show the login page
    return render_template("login.html")

# Note this code is bad. It is handling PII (username, password, phone, email) without encryption
# It would be better if we used OAuth2 and did not need to see or pass around secrets
#
@app_crud.route('/authorize/', methods=["GET", "POST"])
def crud_authorize():
    # check form inputs and creates user
    if request.form:
        # validation should be in HTML
        user_name = request.form.get("user_name")
        phone_number = request.form.get("phone_number")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")           # password should be verified
        # HACK: Verify passwords match
        # we ask for password twice so verify it and if not matching console error and try again
        if (password1 != password2):
            print("Please provide matching passwords")
            return render_template("authorize.html")
        if authorize(user_name, email, password1, phone_number):    
            return redirect(url_for('crud.crud', username=get_login_username()))
    # show the auth user page if the above fails for some reason
    return render_template("authorize.html")

# CRUD logout
@app_crud.route('/logout/', methods=["POST"])
def logout():
    logout_user()
    return render_template('login.html')

# CRUD create/add
@app_crud.route('/create/', methods=["POST"])
def create():
    """gets data from form and add it to Users table"""
    if request.form:
        po = Users(
            request.form.get("name"),
            request.form.get("email"),
            request.form.get("password"),
            request.form.get("phone"), 
            request.form.get("notes")
        )
        po.create()
    return redirect(url_for('crud.crud', username=get_login_username()))


# CRUD read
@app_crud.route('/read/', methods=["POST"])
def read():
    """gets userid from form and obtains corresponding data from Users table"""
    table = [] 
    userid = request.form.get("userid")
    po = user_by_id(userid)
    if po is not None:
        table = [po.read()]  # placed in list for easier/consistent use within HTML
    return render_template("crud.html", table=table)


# CRUD update
@app_crud.route('/update/', methods=["POST"])
def update():
    """gets userid and name from form and filters and then data in  Users table"""

    userid = request.form.get("userid")
    name = request.form.get("name")
    notes = request.form.get("notes")
    po = user_by_id(userid)
    if po is not None:
        po.update(name, "", "", notes)
    return redirect(url_for('crud.crud', username=get_login_username()))



# CRUD delete
@app_crud.route('/delete/', methods=["POST"])
def delete():
    """gets userid from form delete corresponding record from Users table"""

    userid = request.form.get("userid")
    po = user_by_id(userid)
    if po is not None:
        po.delete()
    return redirect(url_for('crud.crud', username=get_login_username()))


# Search Form
@app_crud.route('/search/')
def search():
    """loads form to search Users data"""
    return render_template("search.html")


# Search request and response
@app_crud.route('/search/term/', methods=["POST"])
def search_term():
    """ obtain term/search request """
    req = request.get_json()
    term = req['term']
    response = make_response(jsonify(users_ilike(term)), 200)
    return response
