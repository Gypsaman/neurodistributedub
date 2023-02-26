from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from webproject import db
from webproject.modules.table_creator import Field, TableCreator, timestamp_to_date
from webproject.models import Quizzes, Questions, Answers
from webproject.routes import admin_required
from datetime import datetime as dt


quiz = Blueprint("quiz", __name__)

@quiz.route("/quiz/<int:quiz_id>/<int:question_number>")
@admin_required
def quiz_display(quiz_id,question_number):
    quiz = Quizzes.query.filter_by(id=quiz_id).first()
    all_questions = Questions.query.filter_by(quiz_id=quiz.id).all()
    question = Questions.query.filter_by(quiz_id=quiz.id,display_order=question_number).first()
    answers = Answers.query.filter_by(quiz_id=quiz.id,question_id=question.question_id).all()
    
    return render_template("quizzes/question.html",quiz=quiz,question=question,answers=answers,all_questions=all_questions)
    
@quiz.route("/quiz/<int:quiz_id>/<int:question_number>",methods=['POST'])
@admin_required
def quiz_display_post(quiz_id,question_number):
    quiz = Quizzes.query.filter_by(id=quiz_id).first()
    question = Questions.query.filter_by(quiz_id=quiz.id,display_order=question_number).first()
    number_of_questions = Questions.query.filter_by(quiz_id=quiz.id).count()
    answer_selected = request.form['answer_selected']
    answer = Answers.query.filter_by(quiz_id=quiz.id,question_id=question.question_id,answer_id=answer_selected).first()
    question.answer_chosen = answer.answer_id
    question.is_correct = answer.correct_answer
    db.session.commit()
    
    next_question = (question_number+1) % number_of_questions

    return redirect(url_for("quiz.quiz_display",quiz_id=quiz_id,question_number=next_question))
        
