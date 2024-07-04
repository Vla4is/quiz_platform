from . import db
from flask_login import UserMixin

class Quiz(db.Model):  # inherit model
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    questions = db.relationship('Question', backref='quiz', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # foreignKey ensures that we gave valid user id
    results = db.relationship('Results', backref='quiz', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    answers = db.relationship('Answer', backref='question', lazy=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id')) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # foreignKey ensures that we gave valid user id
    description_title = db.Column(db.String(255))
    description = db.Column(db.String(1000))

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    correct = db.Column(db.Boolean)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # foreignKey ensures that we gave valid user id

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)  # unique = true means that no other user can use this email.
    nickname = db.Column(db.String(255))
    password = db.Column(db.String(255))
    quizzes = db.relationship('Quiz', backref='user', lazy=True)

class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    nickname = db.Column(db.String(255))
    score = db.Column(db.Float)



# from . import db
# from flask_login import UserMixin
# # from sqlalchemy.sql import func
# #may have an errors if i delete nodes
# class Quiz (db.Model): #inherit model
#     id = db.Column (db.Integer, primary_key = True)
#     title = db.Column (db.String (255))
#     questions = db.relationship ('Question')
#     user_id = db.Column (db.Integer, db.ForeignKey ('user.id')) #foreignKey ensures that we gave valid user id
#     results = db.relationship ('Results')

# class Question (db.Model):
#     id = db.Column (db.Integer, primary_key = True)
#     content = db.Column (db.String (255))
#     answers = db.relationship ("Answer")
#     quiz_id = db.Column (db.Integer, db.ForeignKey ("quiz.id")) 
#     user_id = db.Column (db.Integer, db.ForeignKey ('user.id')) #foreignKey ensures that we gave valid user id
#     description_title = db.Column (db.String (255))
#     description = db.Column (db.String (1000))

# class Answer (db.Model):
#     id = db.Column (db.Integer, primary_key = True)
#     content = db.Column (db.String (255))
#     correct = db.Column (db.Boolean)
#     question_id = db.Column (db.Integer, db.ForeignKey ("question.id"))
#     user_id = db.Column (db.Integer, db.ForeignKey ('user.id')) #foreignKey ensures that we gave valid user id

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key = True)
#     email = db.Column (db.String(255), unique = True) #unique = true means that no other user can use this email.
#     nickname = db.Column (db.String (255))
#     password = db.Column (db.String (255))
#     quizzes = db.relationship ('Quiz')

# class Results (db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     quiz_id = db.Column (db.Integer, db.ForeignKey ("quiz.id"))
#     nickname = db.Column (db.String (255))
#     score = db.Column (db.Float)
