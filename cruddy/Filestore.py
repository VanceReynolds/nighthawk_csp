""" database dependencies to support Users db examples """
from __init__ import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import engine_from_config
from sqlalchemy import create_engine


# Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along

# Define the list of files table model
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) Filestore represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Filestore(UserMixin, db.Model):
    # define the filestore schema
    userID = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), unique=False, nullable=False)
    # allow this to be Null  
    notes = db.Column(db.String(255), unique=False, nullable=True)

    # constructor of a User object, initializes of instance variables within object
    def __init__(self, fname, notes):
        self.filename = fname 
        self.notes = notes

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "userID": self.userID,
            "name": self.filename,
            "notes": self.notes,
            "query": "by_alc"  # This is for fun, a little watermark
        }

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD update: updates users name, password, phone
    # returns self
    def update(self, fname, note):
        """only updates values with length"""
        if fname and len(fname) > 0:
            self.filename = fname
        if note and len(note) > 0:
            self.notes = note
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
      
    # required for login_user, overrides id (login_user default) to implemented userID
    def get_id(self):
        return self.userID


def upload_model_tester():
    print("--------------------------")
    print("Seed Data for Table: filestore")
    print("--------------------------")
    db.create_all()
    f1 = Filestore(fname='C:\\Users\\grego\\OneDrive\\Pictures\\Camera\\breaking_boards.jpg', notes='karate')
    f2 = Filestore(fname='C:\\Users\\grego\\OneDrive\\Pictures\\Camera\\GregVegas.JPG', notes="headshot")
    # f3 intended to fail as duplicate key
    table = [f1, f2]
    for row in table:
        try:
            db.session.add(row)
            db.session.commit()
        except IntegrityError:
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {row.email}")

def upload_model_printer():
    print("------------")
    print("Table: users with SQL query")
    print("------------")
    result = db.session.execute('select * from users')
    print(result.keys())
    for row in result:
        print(row)

if __name__ == "__main__":
    upload_model_tester()  # builds model of Users
    upload_model_printer()