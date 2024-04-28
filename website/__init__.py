from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app ():
    app = Flask (__name__)
    app.config ['SECRET_KEY'] = "helllo"
    app.config ['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #database path cofiguration
    db.init_app (app) #ititialize the app to the database

    #creating the paths for the apps
    from .quiz import quiz
    app.register_blueprint (quiz, url_prefix="/")
    
    from .view import view
    app.register_blueprint (view, url_prefix="/")
    
    from .auth import auth
    app.register_blueprint (auth, url_prefix= "/")


    from .models import User
    create_database(app)

    login_manager = LoginManager ()
    login_manager.login_view = 'auth.login'
    login_manager.init_app (app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get (int(id))
    return app

    # from .views import views
    # from .auth import auth
    # app.register_blueprint (views, url_prefix="/")
    # app.register_blueprint (auth, url_prefix="/")


def create_database (app): #app is the application instance
    if not path.exists ('website/' + DB_NAME): #check if database exists
        with app.app_context (): #create database
            db.create_all ()

class CheckCredentials ():
    def __init__(self, u_email =False, u_text = False, u_password=False):
        arr = {}
        if (u_email):
            arr ['email'] =  self.email (u_email)
        if (u_text):
            arr ['text'] = self.text 
        if (u_password):
            arr ['password'] = self.password (u_password)

    @staticmethod
    def email (email):
        if (len (email) < 1):
            return False
        return True
    @staticmethod
    def password(password):
        if (len(password) < 1):
            return False
        return True
    @staticmethod
    def text (text):
        if (len(text) < 1):
            return False
        return True
    @staticmethod
    def all (u_email, u_text,u_password):
        if (CheckCredentials.email (u_email) and CheckCredentials.text (u_text) and CheckCredentials.password(u_password)):
            return True
        else:
            return False