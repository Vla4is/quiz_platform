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
    user_answers = session.get ('user_answers', [])
    
    
    questions = quiz.questions
    
    while (question_live_id < len(questions)-1 and len (questions [question_live_id].answers) <= 0): #Checking the first questions
         question_live_id+=1

    if (len (questions [question_live_id].answers) <=0 and question_live_id == len(questions)-1): #if the quiz is empty
           
            return show_result (0, session['nickname'], "'Empty quiz'")

    answers = questions [question_live_id].answers

    
    
    if request.method == "POST" and request.form.getlist ('single_answer'):
        question_content = str (questions[question_live_id].content)
        user_answers.append({question_content: {"user_answer": [], "correct_answers": []}}) #add the title inside the array
        session['user_answers'] = user_answers
        
        # print (user_wrong_answers.encode('utf-8'))
        

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
                # print (session ['wrong_answers'])
                # user_wrong_answers [user_wrong_answers.len()-1][question_content].append(answers[i].content) #add the content into array
                # session['wrong_answers'] = user_wrong_answers
                current_score-=2
            
            if value:
                user_answers [len (user_answers)-1][question_content]["user_answer"].append (answers[i].content) #no need to add here the session application, but if there is a bug its maybe here
            if answers[i].correct:
                user_answers [len (user_answers)-1][question_content]["correct_answers"].append (answers[i].content) #no need to add here the session application, but if there is a bug its maybe here

            # if answers [i].correct and value == False:
            #     user_wrong_answers [len (user_wrong_answers)-1][question_content].append (answers[i].content) #no need to add here the session application, but if there is a bug its maybe here

                # user_wrong_answers.append("532")
                # session['wrong_answers'] = user_wrong_answers

                
            i+=1
    
        score_to_add = 0
        
        if (possible_score > 0):
            score_to_add = current_score/possible_score

        if (score_to_add > 0):
            total_score += score_to_add

        if (possible_score>0):
            total_possible_score += 1

        question_live_id += 1 

        
        while (question_live_id < len(questions) and len (questions [question_live_id].answers) <= 0): #passing questions without answers in the middle or end.
            question_live_id+=1

        if question_live_id >= len (questions):
            score = 0
            if total_score > 0 and total_possible_score > 0:
                score = round (total_score*10/total_possible_score, 2)
            
            new_result = Results (quiz_id = quiz.id, nickname = session ['nickname'], score = score) #creation of new answer
            db.session.add (new_result) #add this answer into the qerstions
            db.session.commit () #commit the changes
           
            return show_result (new_result.id, session['nickname'], score, session['user_answers'])
        answers = questions [question_live_id].answers
        
        session['total_score'] = total_score
        session['total_possible_score'] = total_possible_score
        session['question_live_id'] = question_live_id
    
    lines = questions [question_live_id].description.count('\n')
    return render_template ("quiz.html", user = current_user, answers = answers, question = questions [question_live_id].content, forScripts = forScripts, description_title = questions [question_live_id].description_title, description = questions [question_live_id].description, lines = lines )

def show_result(id, nickname, score, user_answers = []):
    forScripts = ""
    session.clear ()
    return render_template ("result.html", id = id, nickname = nickname, score = score, user =current_user, forScripts = forScripts, user_answers = user_answers)