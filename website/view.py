from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import current_user
from .models import Quiz, Results
from . import db
from .helpers import CheckCredentials, DisplayMessages, CalculateGrade

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
def enter_nickname (prev_nickname = False):
    
    if (prev_nickname):
        
        session ['nickname'] = prev_nickname
    
    forScripts = ""
    quiz_id = request.args.get ("quizid")
    
    if (session.get ('nickname') != None and quiz_id): 
        
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
    question_live_id = session.get('question_live_id', 0)
    user_answers = session.get ('user_answers', [])
    questions = quiz.questions

    if (question_live_id >= len(questions)): #if the id of the question is more than the answers
        return show_result (55, session['nickname'], 0)
    

    

    if (len(questions) < 1): #in case no questions at all
        return render_template ("undone-quiz.html", user = current_user)
    
    
    # def check_if_no_answers(question_live_id):
    #     while (len (answers) < 1 and (question_live_id >= len(questions))): 
    #         print ("while")
    #         question_live_id+= 1
    #         session ['question_live_id'] = question_live_id
    # check_if_no_answers (question_live_id)
        
    
    

    if request.method == "POST" and request.form.getlist ('single_answer'):
        # print (request.form.getlist ('single_answer'))
        #here i sort the answers, correct and the user answers
        question_title = questions[question_live_id].content
        user_answers.append  ({question_title : {"user_answer" : [], "correct_answer" :[]} }) #add an empty template

        # user_answers[len (user_answers)-1][question_title]["user_answer"] = request.form.getlist ('single_answer') #add the user answer
        #create the correct answers
        for i in range (len (request.form.getlist ('single_answer'))): #we write the answers which user selected
            if request.form.getlist ('single_answer') [i] == "1":
                user_answers[len (user_answers)-1][question_title]["user_answer"].append (questions[question_live_id].answers [i].content)

        for answer in questions [question_live_id].answers:
            if (answer.correct):
                user_answers[len (user_answers)-1] [question_title] ["correct_answer"].append (answer.content) #add the answer
        question_live_id+=1 #adding one to the live id
        session ["user_answers"] = user_answers
        
        session ['question_live_id'] =  question_live_id
        
        
        
    
    if (question_live_id >= len (questions) ) :
        grade = CalculateGrade.standart_decimal (10, user_answers)
        new_result = Results (quiz_id = quiz.id, nickname = session ['nickname'], score = grade) #creation of new answer
        db.session.add (new_result) #add this answer into the qerstions
        db.session.commit () #commit the changes
        
        return show_result (new_result.id, session['nickname'], grade)

    
    while (not questions [question_live_id].answers): #checker if there is no answers
        question_live_id+= 1
        session ['question_live_id'] = question_live_id
        if (question_live_id >= len(questions)):
            grade = CalculateGrade.standart_decimal (10, user_answers)
            new_result = Results (quiz_id = quiz.id, nickname = session ['nickname'], score = grade) #creation of new answer
            db.session.add (new_result) #add this answer into the qerstions
            db.session.commit ()
            return show_result (new_result.id, session['nickname'], grade)


    
    
    return render_template ("quiz.html", user = current_user, answers = questions[question_live_id].answers, question = questions [question_live_id].content, forScripts = forScripts, description_title = questions [question_live_id].description_title, description = questions [question_live_id].description)



def show_result(id, nickname, score):
    forScripts = ""
    quiz_id = request.args.get ("quizid")
    # session.clear ()
    if (request.method == "POST" and request.form.get ("retake_quiz")):
            session ['question_live_id'] = 0
            session ['user_answers'] =  []
            return enter_nickname (nickname)
            
    

    return render_template ("result.html", id = id, nickname = nickname, score = score, user =current_user, forScripts = forScripts, user_answers = session ['user_answers'])