from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from webproject import db
from webproject.modules.table_creator import Field, TableCreator, timestamp_to_date
from webproject.models import Quizzes, Questions, Answers, Quiz_Header, Quiz_Topics
from webproject.routes import admin_required
from datetime import datetime as dt


quiz = Blueprint("quiz", __name__)


@quiz.route('/quizzes')
@login_required
def select_quiz():
    quizzes = db.session.query(Quizzes,Quiz_Header).join(Quiz_Header).filter(Quizzes.user_id==current_user.id).all()
    return render_template("quizzes/quiz_select.html",quizzes=quizzes)

@quiz.route('/quizzes',methods=['POST'])
@login_required
def select_quiz_post():
    quiz_id = request.form['quiz_id']
    quiz = Quizzes.query.filter_by(id=quiz_id).first()
    if quiz.grade is not None:
        return redirect(url_for("quiz.quiz_retake",quiz_id=quiz_id))
    return redirect(url_for("quiz.quiz_grade",quiz_id=quiz_id))

@quiz.route('/quiz/retake/<int:quiz_id>')
@login_required
def quiz_retake(quiz_id):
    quiz = Quizzes.query.filter_by(id=quiz_id).first()
    # quiz.grade = None
    questions = Questions.query.filter_by(quiz_id=quiz.id).all()
    for question in questions:
        question.answer_chosen = ''
    db.session.commit()
    return redirect(url_for("quiz.quiz_display",quiz_id=quiz_id,question_number=1))

@quiz.route('/quiz/<int:quiz_id>')
@login_required
def quiz_grade(quiz_id):
    quiz = Quizzes.query.filter_by(id=quiz_id).first()
    
    if quiz is None or (quiz.user_id != current_user.id and not current_user.id == 1):
        return redirect(url_for("quiz.select_quiz"))
    not_answered = Questions.query.filter_by(quiz_id=quiz.id,answer_chosen='').count()
    
    all_questions = Questions.query.filter_by(quiz_id=quiz.id).count()

    if not_answered == all_questions:
        return redirect(url_for("quiz.quiz_display",quiz_id=quiz_id,question_number=1))
    


    return render_template("quizzes/quiz_grade.html",quiz=quiz,not_answered=not_answered,all_questions=all_questions)

@quiz.route('/quiz/<int:quiz_id>',methods=['POST'])
@login_required
def quiz_grade_post(quiz_id):

    quiz = Quizzes.query.filter_by(id=quiz_id).first()
    all_questions = Questions.query.filter_by(quiz_id=quiz.id).all()
    score = 0
    for question in all_questions:
        if question.is_correct:
            score += 1
    score = score/len(all_questions)*100
    if quiz.grade is None or score > quiz.grade:
        quiz.grade = score
    db.session.commit()
    
    questions = Questions.query.filter_by(quiz_id=quiz.id).order_by(Questions.display_order).all()
    
    question_answers = []
    for question in questions:
        q = {'question':{'display_order':question.display_order,'topic':question.topic,'question':question.question,'answer_chosen':question.answer_chosen,'is_correct':question.is_correct}}
        answers = Answers.query.filter_by(quiz_id=quiz.id,question_id=question.question_id).order_by(Answers.display_order).all()
        q['answers'] = []
        for answer in answers:
            q['answers'].append({'answer_id':answer.answer_id,'display_order':answer.display_order,'answer_txt':answer.answer_txt,'correct_answer':answer.correct_answer})
        question_answers.append(q)
        
    return render_template("quizzes/detailed_grade.html",quiz=quiz,questions=question_answers)
    # return redirect(url_for("quiz.quiz_grade",quiz_id=quiz_id))

@quiz.route("/quiz/<int:quiz_id>/<int:question_number>")
@login_required
def quiz_display(quiz_id,question_number):
    quiz = Quizzes.query.filter_by(id=quiz_id).first()
    all_questions = Questions.query.filter_by(quiz_id=quiz.id).all()
    question = Questions.query.filter_by(quiz_id=quiz.id,display_order=question_number).first()
    if question is None:
        return redirect(url_for("quiz.quiz_display",quiz_id=quiz_id,question_number=1))
    answers = Answers.query.filter_by(quiz_id=quiz.id,question_id=question.question_id).order_by(Answers.display_order).all()
    
    return render_template("quizzes/question.html",quiz=quiz,question=question,answers=answers,all_questions=all_questions)
    
@quiz.route("/quiz/<int:quiz_id>/<int:question_number>",methods=['POST'])
@login_required
def quiz_display_post(quiz_id,question_number):
    quiz = Quizzes.query.filter_by(id=quiz_id).first()
    question = Questions.query.filter_by(quiz_id=quiz.id,display_order=question_number).first()
    number_of_questions = Questions.query.filter_by(quiz_id=quiz.id).count()
    answer_selected = request.form['answer_selected']
    answer = Answers.query.filter_by(quiz_id=quiz.id,question_id=question.question_id,answer_id=answer_selected).first()
    question.answer_chosen = answer.answer_id
    question.is_correct = answer.correct_answer
    db.session.commit()
    
    next_question = question_number+1
    if next_question > number_of_questions:
        next_question = 1

    return redirect(url_for("quiz.quiz_display",quiz_id=quiz_id,question_number=next_question))
        
