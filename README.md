# Valen's Trimester-3 Work

## WIKI Overview Of Work
https://github.com/ValenReynolds/nighthawk_csp/wiki/TT3-Assignment 

##TT3 Challenges/Hacks:
* Hack #1 Added Phone Number to Sign Up screen
* Hack #2 Added logout to CRUD screen.
* Hack #3 Added a login required to Fibonacci page

## Additional features added to the project:
* HACK #4 Added a "Remember Me" check box to the login page. Passed a 3 minute time out when remember me is not checked. Changed remember me timeout to 1 day.
* HACK #5 Validated email/password on login page. Print error to console if "Invalid username and/or password"
* HACK #6 Validated email, check for duplicate email on sign up page. Print error to console "Email already in user by another registered user "
* HACK #7 Validated passwords match on create login page. Print error to console "Please provide matching passwords"
* HACK #8 Displayed logged in User on top of CRUD Page
* Hack #9 Added login/logout to navbar
* Hack #10 Automatically log out previously logged in user at the login screen
* Hack #11 Identify "anonymous" username on CRUD Page if no longer logged in
* Hack #12 Update now allows phone number, name, email to be updated with better styling of form
* Hack #13 Database has a new field notes, table supports notes view
* Hack #14 Create now supports creating new users with a "notes" entry
* Hack #15 Update supports new "notes" field

@app_crud.route('/update/', methods=["POST"])
def update():
    """gets userid and name from form and filters and then data in  Users table"""

    userid = request.form.get("userid")
    name = request.form.get("name")
    phone = request.form.get("phone")
    email = request.form.get("email")
    notes = request.form.get("notes")
    po = user_by_id(userid)
    if po is not None:
        po.update(name, "", phone, notes, email)
    return redirect(url_for('crud.crud', username=get_login_username()))

## Upload Project Addition
* https://github.com/nighthawkcoders/nighthawk_csp/wiki/Tri-3:-Tech-Talk-Week-10:-Uploading-content-to-a-Web-Site
* 
* Hack #0 Add the upload.html, app_content.py to project. Create a Blueprint() for app_content and added to main.py. Add "Upload" to navbar
** Once a user logs in they can now use the upload page we were given to start

## Future Work
Based on Google searching I think these require javascript to modify the html pages? Need some help.
* Navbar grey options that do not apply with .css and javascript (hard!)
* Add lock symbol to menu items when running as anonymous (more hard javascript and .css / html )

## Replit Work

Link to Replit https://replit.com/@valenryanreynol/Valen-Tri-3-Work#.replit

## Commits
I am not using pull requests. Commits are made to master directly from my windows laptop or slow school laptop 
Hope this is ok?

https://github.com/ValenReynolds/nighthawk_csp/commits/master 
