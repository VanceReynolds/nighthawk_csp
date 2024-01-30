import logging
import os

''' import boto3 '''

from __init__ import app
''' from botocore.exceptions import ClientError '''
from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from cruddy.Filestore import Filestore, filestore_by_id
from cruddy.query import user_by_id

# blueprint defaults https://flask.palletsprojects.com/en/2.0.x/api/#blueprint-objects
app_content = Blueprint('content', __name__,
                        url_prefix='/content',
                        template_folder='templates/cruddy/',
                        static_folder='static',
                        static_url_path='static')

''' 
Objective of the ideas started with this page is to manage uploading content to a Web Site
Code provided allows user to upload Image into static/uploads folder 
'''
# ... An Image is often called a picture, it works with <image ...> tage in HTML
# ... Supported types jpeg, gif, png, apng, svg, bmp, bmp ico, png ico.

'''
Hack #1 add additional content
'''
# Additional Content
# ... Video, Comma Seperated Values (CSV), Code File (py,java)
# ... One or more uploading capabilities can be provided to support needs of your project

'''
Hack #2 add additional description and capabilities
'''
# Establish a database record that keeps track of content and establishes meta data
# ... user who uploaded
# ... description
# Combine Note and Image upload into single activie
# ... description of Note is Markdown text
# ... try using uploaded image in notes
# ... think about easier markdown UI for user of Note and Images

'''
Hack #3 establish a strategy to manage data being stored through Amazon S3 bucket
'''
# AWS S3 Object Container is a system used to manage content
# ... S3 Bucket Concept: https://www.youtube.com/watch?v=-VVC7uTNJX8


# A global variable is used to provide feedback for session to users, but is considered short term solution
files_uploaded = []


# Page to upload content page
@app_content.route('/')
@login_required
def content():
    # grab user object (uo) based on current login
    uo = user_by_id(current_user.userID)
    user = uo.read()  # extract user record (Dictionary)
    # load content page passing user and list of uploaded files
    
    return render_template("content.html", table=filespace_all(), user=user)
   # return render_template('content.html', user=user, files=files_uploaded)

ALLOWED_EXTENSIONS = set(['csv','jpg','png','gif','mp4'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# SQLAlchemy extract all users from database
def filespace_all():
    table = Filestore.query.all()
    json_ready = [peep.read() for peep in table]
    return json_ready


# Content delete
@app_content.route('/delete/', methods=["POST"])
def delete():
    """gets userid from form delete corresponding record from Users table"""

    userid = request.form.get("userid")
    fs = filestore_by_id(userid)
    if fs is not None:
        fs.delete() 
        return redirect(url_for("content.content", table=filespace_all()))
    else:
        return redirect(url_for('content.content'))


# Notes create/add
@app_content.route('/upload/', methods=["POST"])
@login_required
def upload():
    try:
        
    # grab user object (uo) based on current login
        uo = user_by_id(current_user.userID)
        user = uo.read()  # extract user record (Dictionary)
        logging.basicConfig(level=logging.DEBUG, filename='nighthawk_csp.log')

        # grab file object (fo) from user input
        # The fo variable holds the submitted file object. This is an instance of class FileStorage, which Flask imports from Werkzeug.
        fo = request.files['filename']

        # throw 400 error if file type not supported
        if not allowed_file(fo.filename):
            abort (400)
            
        # save file to location defined in __init__.py
        # ... os.path uses os specific pathing for web server
        # ... secure_filename checks for integrity of name for operating system. Pass it a filename and it will return a secure version of it.
      
      # S3 requires we use a secure filename - we need this for later
      # right now secure_filename is returning nothing so we are skipping it (useless)
      #  secure_name = os.path.join(app.config['Secure this'], secure_filename(fo.filename))
        secure_name = './static/uploads/' + fo.filename    
        fo.save(secure_name)
    
        po = Filestore(
            fo.filename, 
            request.form.get("notes")
        )
        po.create() 

        # upload to S3 server
        upload_s3_file (fo.filename, 'gid-requests', 'gid-requests_2022_06_06')

        return redirect(url_for("content.content", table=filespace_all(), user=user))

       # files_uploaded.insert(0, url_for('static', filename='uploads/' + fo.filename))
    except Exception as ex:
        print (ex)
        # errors handled, but specific errors are not messaged to user
        logging.exception("Error:")
        # pass
    # reload content page
    return redirect(url_for('content.content'))


def upload_s3_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    s3 = boto3.client('s3')
with open("FILE_NAME", "rb") as f:
    s3.upload_fileobj(f, "BUCKET_NAME", "OBJECT_NAME")

s3.upload_file(
    'FILE_NAME', 'BUCKET_NAME', 'OBJECT_NAME',
    ExtraArgs={'Metadata': {'mykey': 'myvalue'}}
)
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3', region_name = 'us-west-2')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

