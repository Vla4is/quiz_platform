from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from flask_login import login_required, current_user
from . import db
from .helpers import DisplayMessages
from .models import Quiz, Question, Answer
from .constructor import t1_data_constructor
advanced = Blueprint ('advanced', __name__)
@advanced.route ("/constructor", methods = ['GET', 'POST'])
@login_required
def constructor ():
    #get the quiz
    quiz_id = request.args.get('quizid')

    quiz = Quiz.query.get (quiz_id)
    if (not quiz) or quiz.user_id != current_user.id: #redirect if there is no quiz like this
        
        return redirect (url_for ('view.join'))
    forScripts = ""
    text = ""
    
    dm = DisplayMessages ()
    if (session.get ('for_scripts')):
        forScripts = session.get ('for_scripts')
        session.clear ()
    
    if request.method == 'POST' :
        
        text = request.form.get ("constructor_data")
        
        sorted_data = t1_data_constructor (text)
        # print (sorted_data)
        for set in sorted_data.items():
            question = set[1][0]
            
            description_title = ""
            description = ""
            if (len (set[1]) == 4):
                description_title = set [1][2]
                description = set [1][3]

            ##TRIM THE STARTS IN THE BEGGINING
            if question.startswith("**"):
                question = question[2:]
            if question.endswith("**"):
                question = question[:-2]
            print (description_title, description)
            new_question = Question (quiz_id = quiz_id, content = question, user_id = current_user.id, description_title = description_title, description = description)
            db.session.add (new_question)
            db.session.commit ()
            for answer in set [1][1].items():
                single_answer = answer [1]
                new_answer = Answer (question_id = new_question.id, content = single_answer [0], user_id = current_user.id, correct =single_answer [1]) #creation of new answer
                db.session.add (new_answer) #add this answer into the qerstions
                db.session.commit ()
            forScripts = dm.green ("Constructed succesfully")
                
        
    
    return render_template ("constructor.html", user = current_user, forScripts=forScripts, quiz = quiz, text = text)
