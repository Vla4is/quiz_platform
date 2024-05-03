from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .helpers import DisplayMessages
from .models import Quiz, Question, Answer
import json

quiz = Blueprint ('quiz', __name__)

@quiz.route ("/manage", methods = ['GET', 'POST'])
@login_required
def manage ():
    forScripts = ""
    quizOrder = 0
    if request.method == 'POST':
    
        if (request.form.get ("quizname")): #add new quiz
            data = request.form.get ("quizname")
            newQuiz = Quiz (title = data, user_id = current_user.id)
            db.session.add (newQuiz)
            db.session.commit ()
        elif (request.form.get ("edit_quizname")):
            quiz_id = request.form.get ("quiz_id")
            new_title = request.form.get ("edit_quizname")
            quiz = Quiz.query.filter_by(id = quiz_id , user_id=current_user.id).first()
            if quiz:
                quiz.title = new_title
                db.session.commit()
        else:
            dm = DisplayMessages ()
            forScripts = dm.red ("Wrong input")
    
    return render_template ("manage.html", user = current_user, forScripts=forScripts)

@login_required
@quiz.route ('/delete-quiz', methods = ['POST'])
def delete_note (): ##delete quiz
    
    quiz = json.loads (request.data)
    quizId = quiz ['quiz_id']
    quiz = Quiz.query.get (quizId)
    
    if quiz:
        if quiz.user_id == current_user.id:
            db.session.delete (quiz)
            db.session.commit()
    return jsonify({})

@login_required
@quiz.route ('/edit-questions', methods = ['POST', 'GET'])
def edit_questions ():
    forScripts=""
    quiz_id = request.args.get('quizid')
    # print(quiz_id)
    quiz = Quiz.query.get (quiz_id)
    if (not quiz) or quiz.user_id != current_user.id: #redirect if there is no quiz like this
        return redirect (url_for ('view.join'))
    
    else: #everything is fine and we can proceed to the question addition or edit
        questions = Question.query.filter_by(quiz_id = quiz_id).all()
        
        if request.method == 'POST': #add new quiz
            
            if request.form.get ("new_question"):
                question = request.form.get ("new_question")
                new_question = Question (quiz_id = quiz_id, content = question, user_id = current_user.id)
                db.session.add (new_question)
                db.session.commit ()
                return redirect(url_for('quiz.edit_questions', quizid=quiz_id))
            else:
                dm = DisplayMessages ()
                forScripts = dm.red ("Wrong input")
            ###END OF ADD NEW QUIZ
        return render_template ("edit-questions.html", questions = questions, user = current_user, quiz_name = quiz.title, forScripts=forScripts)
        #try to get data of questions

@login_required
@quiz.route ('/delete-question', methods = ['POST'])
def delete_question ():
    question = json.loads (request.data)
    question = question ['question_id']
    
    question = Question.query.get (question)
    
    if question:
        db.session.delete (question)
        db.session.commit()
    return jsonify({})

@login_required
@quiz.route ('/update-question', methods = ['GET', 'POST'])
def update_question ():
    question = json.loads (request.data)
    new_content = question ['new_value']
    question_id = question ['question_id']
    question = Question.query.get (question_id)
    if question:       # Update the question title
        question.content = new_content
        db.session.commit()

    return jsonify({})

@login_required
@quiz.route ('/edit-answers', methods = ['POST', 'GET'])
def edit_answers (): #edit answers page
    forScripts=""
    question_id = request.args.get('questionid') #Get the question id
    question = Question.query.get (question_id) #get the quiestion
    if (not question) or question.user_id != current_user.id: #redirect if there is no quiz like this
        return redirect (url_for ('view.join'))
    
    else: #everything is fine and we can proceed to the question addition or edit
        answers = Answer.query.filter_by(question_id = question_id).all() ##get all the answers with this question id
        if request.method == 'POST':
            if (request.form.get ("new_answer")): #add new quiz
                answer = request.form.get ("new_answer") #put into the variable
                new_answer = Answer (question_id = question_id, content = answer, user_id = current_user.id, correct = False) #creation of new answer
                db.session.add (new_answer) #add this answer into the qerstions
                db.session.commit () #commit the changes
                return redirect(url_for('quiz.edit_answers', questionid=question_id))
            else: 
                dm = DisplayMessages ()
                forScripts = dm.red ("Wrong input")
            ###END OF ADD NEW QUIZ 
        return render_template ("edit-answers.html", answers = answers, user = current_user, question=question, forScripts=forScripts)
        #try to get data of questions


@login_required
@quiz.route ('/change-answer-state', methods = ['POST', 'GET'])
def change_answer_state ():
    
    question = json.loads (request.data)
    new_state = question ['new_state']

    answer_id = question ['answer_id']
    answer = Answer.query.get (answer_id)
    if answer:       # Update the question title
        answer.correct = new_state
        db.session.commit()
    return jsonify({})

@login_required
@quiz.route ('/delete-answer', methods = ['POST'])
def delete_answer ():
    answer = json.loads (request.data)
    answer_id = answer ['answer_id']
    answer = Answer.query.get (answer_id)
    if answer and answer.user_id == current_user.id:
        db.session.delete (answer)
        db.session.commit()
    return jsonify({})

@login_required
@quiz.route ('/update-answer', methods = ['GET', 'POST'])
def update_answer ():
    answer = json.loads (request.data)
    new_content = answer ['new_value']
    answer_id = answer ['answer_id']
    answer = Answer.query.get (answer_id)
    if answer and answer.user_id == current_user.id:       # Update the question title
        answer.content = new_content
        db.session.commit()
    return jsonify({})

@login_required
@quiz.route ('/results', methods = ['GET', 'POST'])
def results ():
    forScripts=""
    quiz_id = request.args.get ("quizid")
    # print (quiz_id)
    quiz = Quiz.query.get (quiz_id)
    if (current_user.id != quiz.user_id):
        return redirect(url_for('quiz.join'))
    else:
        db.session.commit()
        return render_template ("results.html", user = current_user, results = quiz.results, quiz = quiz, forScripts="") # results = quiz.resutls, quizname = quiz.title
    
@quiz.route ('/delete-result', methods = ['GET', 'POST'])
def delete_result (): #add here messages
    
    quiz = json.loads (request.data)
    result_id = quiz ['result_id']
    quiz_id = quiz ['quiz_id']
    quiz = Quiz.query.get (quiz_id)


    if quiz and quiz.user_id == current_user.id:
        result_to_delete = None
        for result in quiz.results:
            if result_id == "all":
                db.session.delete(result)
                
            elif result.id == result_id:
                result_to_delete = result
                break
        if result_to_delete:
            db.session.delete(result_to_delete)
            db.session.commit()
        elif result_id == "all":
            db.session.commit()
        
    return jsonify({})

