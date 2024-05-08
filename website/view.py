from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import current_user
from .models import Quiz, Results
from . import db
from .helpers import CheckCredentials, DisplayMessages

view = Blueprint ('view', __name__)

@view.route ("/", methods = ['GET', 'POST'])
def join ():
    forScripts = ""

    if (request.method == "POST"):

        session.clear()
        quiz_id = request.form.get ('quiz_id')

        load_quiz = Quiz.query.filter_by(id = quiz_id).first()
        if (load_quiz):
            return redirect(url_for('view.enter_nickname', quizid=quiz_id))  # Redirect to enter_nickname
        else:
            check_credentials = CheckCredentials ()
            check_credentials = check_credentials.text (quiz_id)
            if (check_credentials == True):
                dm = DisplayMessages ()
                forScripts = dm.red ("Wrong quiz pin")
            else:
                forScripts = check_credentials
    return render_template ("join.html", user = current_user, forScripts = forScripts)

@view.route ("/enter-nickname", methods = ['GET', 'POST'])
def enter_nickname ():
    forScripts = ""
    quiz_id = request.args.get ("quizid")
    
    if (session.get ('nickname') != None and quiz_id == session.get('quizid')): 
        load_quiz = Quiz.query.filter_by(id = quiz_id).first ()
        return quiz_page(load_quiz)
    else:
        session.clear ()
    if (request.method == "POST"):
        nickname = request.form.get ('nickname')
        if (nickname):
            load_quiz = Quiz.query.filter_by(id = quiz_id).first ()
            session['quizid'] = quiz_id
            session['nickname'] = nickname
            return quiz_page(load_quiz)
        else:
            dm = DisplayMessages ()
            forScripts = dm.red ("Please enter proper nickname")

    return render_template ("enter-nickname.html", user = current_user, forScripts = forScripts)


@view.route ("/quiz", methods = ['GET', 'POST'])
def quiz_page (quiz):
    forScripts = ""
    total_score = session.get('total_score', 0)
    total_possible_score = session.get('total_possible_score', 0)
    question_live_id = session.get('question_live_id', 0)
    
    questions = quiz.questions 
    
    answers = questions [question_live_id].answers
    if request.method == "POST" and request.form.getlist ('single_answer'):
        values = request.form.getlist ('single_answer')
        i =0
        current_score = 0
        possible_score = 0
        for value in values:
            if value == "1": value = True #convert to boolean
            else: value = False
            if answers [i].correct and value == True:
                current_score+=1
                possible_score+=1

            elif answers [i].correct:
                possible_score += 1

            elif not answers [i].correct and value == True:
                current_score-=2
                
            i+=1
    
        score_to_add = 0
        
        if (possible_score > 0):
            score_to_add = current_score/possible_score

        if (score_to_add > 0):
            total_score += score_to_add

        if (possible_score>0):
            total_possible_score += 1

        question_live_id += 1 
    
        if question_live_id >= len (questions):
            score = round (total_score*10/total_possible_score, 2)
            new_result = Results (quiz_id = quiz.id, nickname = session ['nickname'], score = score) #creation of new answer
            db.session.add (new_result) #add this answer into the qerstions
            db.session.commit () #commit the changes
           
            return show_result (new_result.id, session['nickname'], score)
        answers = questions [question_live_id].answers
        
        session['total_score'] = total_score
        session['total_possible_score'] = total_possible_score
        session['question_live_id'] = question_live_id
    
        
    return render_template ("quiz.html", user = current_user, answers = answers, question = questions [question_live_id].content, forScripts = forScripts)

def show_result(id, nickname, score):
    forScripts = ""
    session.clear ()
    return render_template ("result.html", id = id, nickname = nickname, score = score, user =current_user, forScripts = forScripts)