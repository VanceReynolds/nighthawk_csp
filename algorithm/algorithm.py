from __init__ import login_manager
from flask import Blueprint, render_template, request, url_for, redirect, jsonify, make_response
from flask_login import login_required

from .fibonacci import Fibonacci
from .palindrome import Palindrome

# blueprint defaults https://flask.palletsprojects.com/en/2.0.x/api/#blueprint-objects
app_fibonacci = Blueprint('crud', __name__,
                     url_prefix='/crud',
                     template_folder='templates/cruddy/:templates/:algorithms/templates/',
                     static_folder='static',
                     static_url_path='static')

 
# If you decorate a view(route) with this, it will ensure that the current user is logged in and authenticated before calling the actual view. 
# (If they are not, it calls the LoginManager.unauthorized callback.). 
# Use this example for Hack #3.
@app_fibonacci.route('/')
@app_fibonacci.route('/palindrome/')
@login_required  # Flask-Login uses this decorator to restrict access to logged in users
def fibonacci():
    """obtains all Users from table and loads Admin Form"""    
    if request.form:
        return render_template("fibonacci.html", fibonacci=Fibonacci(int(request.form.get("series"))))
    return render_template("fibonacci.html", fibonacci=Fibonacci(2))

# Unauthorised users do not get access to the Fibonacci
# Flask-Login directs unauthorised users to this unauthorized_handler
@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    return redirect(url_for('crud.crud_login'))


app_algorithm = Blueprint('algorithm', __name__,
                          url_prefix='/algorithm',
                          template_folder='templates/algorithm',
                          static_folder='static',
                          static_url_path='assets')


@app_algorithm.route('/fibonacci/', methods=["GET", "POST"])
def fibonacci():
    if request.form:
        return render_template("fibonacci.html", fibonacci=Fibonacci(int(request.form.get("series"))))
    return render_template("fibonacci.html", fibonacci=Fibonacci(2))


@app_algorithm.route('/palindrome/', methods=["GET", "POST"])
def palindrome():
    if request.form:
        return render_template("palindrome.html", palindrome=Palindrome(request.form.get("candidate")))
    return render_template("palindrome.html", palindrome=Palindrome("a toyota"))
