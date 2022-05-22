from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

dbURI = 'sqlite:///model/myDB.db'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = dbURI  

db = SQLAlchemy(app)
migrate = Migrate(app, db) 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String(128))