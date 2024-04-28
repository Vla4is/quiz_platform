from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from . import CheckCredentials, db
from  .models import User
auth = Blueprint ('auth', __name__)

@auth.route ("/register", methods = ['GET', 'POST'])
def register ():
    if (current_user.is_authenticated):
        return redirect (url_for ('view.join')) 
    
    email = request.form.get ("email")
    nickname = request.form.get ("nickname")
    password = request.form.get ("password")
    validate_password = request.form.get ("validatepassword")

    if password == validate_password and request.method == "POST" and CheckCredentials.all (email, nickname, password) :
        #######################DONT FORGET TO DO PASSWORD HASH LATER####################
        #DISPLAY ERRORS!
        new_user = User (email = email, password = password, nickname = nickname)
        db.session.add (new_user)
        db.session.commit ()
        return redirect (url_for ('view.join'))
    # else:
    #     print ("Wrong Credentials")

    return render_template ("register.html", user = current_user)
@auth.route ("/login", methods = ['GET', 'POST'])
def login():

    if (current_user.is_authenticated):
        return redirect (url_for ('view.join')) 
    #DISPLAY ERRORS!########################################
    if request.method == "POST":
        email = request.form.get ("email")
        password = request.form.get ('password')
        if (CheckCredentials.all (email, "passing text", password)):
            user = User.query.filter_by (email = email).first()
            if user and user.password == password:#ADD HASH LATER
                login_user (user, remember = True)
                return redirect (url_for ('view.join'))

    return render_template("login.html", user = current_user)
@login_required
@auth.route ('/logout')
def logout():
    logout_user()
    return redirect (url_for ('view.join'))
