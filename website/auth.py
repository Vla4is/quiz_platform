from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .helpers import CheckCredentials, CheckDB, DisplayMessages
from  .models import User
auth = Blueprint ('auth', __name__)

@auth.route ("/register", methods = ['GET', 'POST'])
def register ():

    checkCredentials = CheckCredentials()
    forScripts = ""

    if (current_user.is_authenticated):
        return redirect (url_for ('view.join')) 
    
    email = request.form.get ("email")
    nickname = request.form.get ("nickname")
    password = request.form.get ("password")
    validate_password = request.form.get ("validatepassword")
    if request.method == "POST":

        checkCredentials = checkCredentials.all (email, nickname, password)
        if (checkCredentials == True):
            check_db = CheckDB()
            email_exists = check_db.email (email)
            if email_exists:
                checkCredentials = email_exists

        if password == validate_password and request.method == "POST" and checkCredentials == True :
            #######################DONT FORGET TO DO PASSWORD HASH LATER####################
            #DISPLAY ERRORS!
            new_user = User (email = email, password = password, nickname = nickname)
            db.session.add (new_user)
            db.session.commit ()
            return redirect (url_for ('view.join'))
        else:

            forScripts = checkCredentials
            print (forScripts)

    return render_template ("register.html", user = current_user, forScripts = forScripts, entered_nickname = nickname, entered_email = email)
@auth.route ("/login", methods = ['GET', 'POST'])
def login():
    email = ""
    forScripts = ""
    if (current_user.is_authenticated):
        return redirect (url_for ('view.join')) 
    #DISPLAY ERRORS!########################################
    if request.method == "POST":
        email = request.form.get ("email")
        password = request.form.get ('password')
        checkCredentials = CheckCredentials ()
        checkCredentials = checkCredentials.all (email, "passing text", password)
        if (checkCredentials == True): #if there is invalid format don't even access the database.
            user = User.query.filter_by (email = email).first()
            if user and user.password == password:
                login_user (user, remember = True)
                return redirect (url_for ('view.join'))
            else:
                dm = DisplayMessages ()
                forScripts = dm.red ("Wrong credentials")


        else:
            forScripts = checkCredentials

    return render_template("login.html", user = current_user, forScripts = forScripts, entered_email = email)
@login_required
@auth.route ('/logout')
def logout():
    logout_user()
    return redirect (url_for ('view.join'))
