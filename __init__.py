from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Setup of key Flask object (app)
app = Flask(__name__)
dbURI = 'sqlite:////home/vancer/vscode/nighthawk_csp/model/myDB.db'
# Setup SQLAlchemy object and properties for the database (db)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = dbURI
app.config['SECRET_KEY'] = 'SECRET_KEY'
db = SQLAlchemy(app)
Migrate(app, db)
# Setup LoginManager object (app)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
