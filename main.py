from flask import render_template
from __init__ import app

from cruddy.app_starter import app_starter
from api.webapi import app_api
from cruddy.app_crud import app_crud
from cruddy.app_content import app_content
from cruddy.app_crud_api import app_crud_api
from frontend.frontend import app_frontend

app.register_blueprint(app_starter)
app.register_blueprint(app_api)
app.register_blueprint(app_crud)
app.register_blueprint(app_content)
app.register_blueprint(app_crud_api)
app.register_blueprint(app_frontend)


@app.route('/')
def index():
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == "__main__":
    # runs the application on the repl development server
    app.run(debug=True, port="5222")
