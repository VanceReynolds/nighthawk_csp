""" database dependencies to support Users db examples """
from __init__ import db
from __init__ import dbURI
from alembic import op
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import engine_from_config
from sqlalchemy.engine import reflection
from sqlalchemy import create_engine

# check if a column exists in the database and if it does return True, else return False and add the column
def _table_has_column(table, column):
   # config = db.get_context().config
   # engine = engine_from_config(config.get_section(config.config_ini_section), prefix='sqlalchemy.')
    engine = create_engine(dbURI)
    insp = reflection.Inspector.from_engine(engine)
    has_column = False
    for col in insp.get_columns(table):
        if column not in col['name']:
            continue
        has_column = True
    return has_column

# extend database adding a new 'notes' column using alembic 
# see https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script
def add_column(column_name):
    op.add_column(column_name, sa.Column('last_transaction_date', sa.DateTime))
        


# Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along

# Define the Users table within the model
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) Users represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Users(UserMixin, db.Model):
    # define the Users schema
    userID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    phone = db.Column(db.String(255), unique=False, nullable=False)
    # must allow this to be Null since it was added before data existed
    notes = db.Column(db.String(255), unique=False, nullable=True)

    # constructor of a User object, initializes of instance variables within object
    def __init__(self, name, email, password, phone, notes=""):
        self.name = name
        self.email = email
        self.set_password(password)
        self.phone = phone
        self.notes = notes

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "userID": self.userID,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "phone": self.phone,
            "notes": self.notes,
            "query": "by_alc"  # This is for fun, a little watermark
        }

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from Users(db.Model) class, passes initializers
            if _table_has_column('users', 'notes') == False:
                op.add_column('notes', sa.Column('last_transaction_date', sa.DateTime))

            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None



    # CRUD update: updates users name, password, phone
    # returns self
    def update(self, name, email, password, phone, note=""):
        """only updates values with length"""
        if name and len(name) > 0:
            self.name = name
        if password and len(password) > 0:
            self.set_password(password)
        if phone and len(phone) > 0:
            self.phone = phone
        if note and len(note) > 0:
            self.notes = note
        if email and len(email) > 0:
            self.email = email
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

    # set password method is used to create encrypted password
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    # check password to check versus encrypted password
    def is_password_match(self, password):
        """Check hashed password."""
        result = check_password_hash(self.password, password)
        return result

    # required for login_user, overrides id (login_user default) to implemented userID
    def get_id(self):
        return self.userID


"""Database Creation and Testing section"""


def model_tester():
    print("--------------------------")
    print("Seed Data for Table: users")
    print("--------------------------")
    db.create_all()
    """Tester data for table"""
    u1 = Users(name='Thomas Edison', email='tedison@example.com', password='123toby', phone="1111111111")
    u2 = Users(name='Nicholas Tesla', email='ntesla@example.com', password='123niko', phone="1111112222")
    u3 = Users(name='Alexander Graham Bell', email='agbell@example.com', password='123lex', phone="1111113333")
    u4 = Users(name='Eli Whitney', email='eliw@example.com', password='123whit', phone="1111114444")
    u5 = Users(name='John Mortensen', email='jmort1021@gmail.com', password='123qwerty', phone="8587754956")
    u6 = Users(name='John Mortensen', email='jmort1021@yahoo.com', password='123qwerty', phone="8587754956")
    # U7 intended to fail as duplicate key
    u7 = Users(name='John Mortensen', email='jmort1021@yahoo.com', password='123qwerty', phone="8586791294")
    table = [u1, u2, u3, u4, u5, u6, u7]
    for row in table:
        try:
            db.session.add(row)
            db.session.commit()
        except IntegrityError:
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {row.email}")


def model_printer():
    print("------------")
    print("Table: users with SQL query")
    print("------------")
    result = db.session.execute('select * from users')
    print(result.keys())
    for row in result:
        print(row)


if __name__ == "__main__":
    model_tester()  # builds model of Users
    model_printer()
