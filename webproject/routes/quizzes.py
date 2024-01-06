from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from webproject import db
from webproject.modules.table_creator import Field, TableCreator, timestamp_to_date,round_to_2_decimals
from webproject.models import Quizzes, Questions, Answers, Quiz_Header, Quiz_Topics, Quiz_DueDates, Sections
from webproject.modules.quizzes import Topics

from webproject.routes import admin_required
from datetime import datetime as dt
from webproject.modules.quizzes import create_quiz_users
from webproject.modules.logger import Log, LogType
from sqlalchemy import text


quiz = Blueprint("quiz", __name__)


@quiz.route('/quizzes')
@login_required
def select_quiz():
    quizzes = db.session.query(Quizzes,Quiz_Header).join(Quiz_Header).filter(Quizzes.user_id==current_user.id,Quiz_Header.active==True).all()
    return render_template("quizzes/quiz_select.html",quizzes=quizzes)

@quiz.route('/quizzes',methods=['POST'])
@login_required
def select_quiz_post():
    quiz_id = request.form['quiz_id']
    quiz = Quizzes.query.filter_by(id=quiz_id).first()
    Log(LogType.QUIZ,current_user.student_id,f"Quiz {quiz_id}")
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
        question.is_correct = None
    db.session.commit()
    return redirect(url_for("quiz.quiz_display",quiz_id=quiz_id,question_number=1))

@quiz.route('/quiz/<int:quiz_id>')
@login_required
def quiz_grade(quiz_id):
    

    
    quiz = Quizzes.query.filter_by(id=quiz_id).first()
    
    if quiz is None or (quiz.user_id != current_user.id and not current_user.id == 1):
        return redirect(url_for("quiz.select_quiz"))
    not_answered = Questions.query.filter_by(quiz_id=quiz.id,answer_chosen=0).count()
    
    all_questions = Questions.query.filter_by(quiz_id=quiz.id).count()

    if not_answered == all_questions:
        return redirect(url_for("quiz.quiz_display",quiz_id=quiz_id,question_number=1))
    


    return render_template("quizzes/quiz_grade.html",quiz=quiz,not_answered=not_answered,all_questions=all_questions)

@quiz.route('/quiz/<int:quiz_id>',methods=['POST'])
@login_required
def quiz_grade_post(quiz_id):

    quiz = Quizzes.query.filter_by(id=quiz_id).first()
    date_due = Quiz_DueDates.query.filter_by(quiz_header=quiz.quiz_header,section=current_user.section).first().date_due
    all_questions = Questions.query.filter_by(quiz_id=quiz.id).all()
    score = 0
    for question in all_questions:
        if question.is_correct:
            score += 1
    score = score/len(all_questions)*100
    penalty = 0
    if dt.now() > date_due:
        days = (dt.now() - date_due).days
        penalty = 5 if days < 7 else  11
        penalty = 15 if days > 21 else penalty 
        score = max(score - penalty,0)
    if quiz.grade is None or score > quiz.grade:
        quiz.grade = score
    db.session.commit()
    
    questions = Questions.query.filter_by(quiz_id=quiz.id).order_by(Questions.display_order).all()
    
    question_answers = []
    for question in questions:
        q = {'question':{'display_order':question.display_order,'topic':question.topic,'question':question.question,'answer_chosen':question.answer_chosen,'is_correct':question.is_correct}}
        answers = Answers.query.filter_by(question_id=question.question_id).order_by(Answers.display_order).all()
        q['answers'] = []
        for answer in answers:
            q['answers'].append({'answer_id':answer.answer_id,'display_order':answer.display_order,'answer_txt':answer.answer_txt,'correct_answer':answer.correct_answer})
        question_answers.append(q)
        
    return render_template("quizzes/detailed_grade.html",quiz=quiz,questions=question_answers,score=score,penalty=penalty)
    # return redirect(url_for("quiz.quiz_grade",quiz_id=quiz_id))

@quiz.route("/quiz/<int:quiz_id>/<int:question_number>")
@login_required
def quiz_display(quiz_id,question_number):
    quiz = Quizzes.query.filter_by(id=quiz_id).first()
    all_questions = Questions.query.filter_by(quiz_id=quiz.id).all()
    question = Questions.query.filter_by(quiz_id=quiz.id,display_order=question_number).first()
    if question is None:
        return redirect(url_for("quiz.quiz_display",quiz_id=quiz_id,question_number=1))
    answers = Answers.query.filter_by(question_id=question.question_id).order_by(Answers.display_order).all()
    
    return render_template("quizzes/question.html",quiz=quiz,question=question,answers=answers,all_questions=all_questions)
    
@quiz.route("/quiz/<int:quiz_id>/<int:question_number>",methods=['POST'])
@login_required
def quiz_display_post(quiz_id,question_number):
    quiz = Quizzes.query.filter_by(id=quiz_id).first()
    question = Questions.query.filter_by(quiz_id=quiz.id,display_order=question_number).first()
    number_of_questions = Questions.query.filter_by(quiz_id=quiz.id).count()
    answer_selected = request.form['answer_selected']
    answer = Answers.query.filter_by(question_id=question.question_id,answer_id=answer_selected).first()
    question.answer_chosen = answer.answer_id
    question.is_correct = answer.correct_answer
    db.session.commit()
    
    next_question = question_number+1
    if next_question > number_of_questions:
        next_question = 1

    return redirect(url_for("quiz.quiz_display",quiz_id=quiz_id,question_number=next_question))
        


@quiz.route('/view_quizzes/<int:page_num>')
@admin_required
def view_quizzes(page_num):
    
    fields = {
        'id': Field(None,None),
        'description': Field(None,'Description'),
        'multiple_retries': Field(None,'Multiple Retries'),
        'active': Field(None,'Active'),
        'grade_category': Field(None,'Grade Category')
    }

    table_creator = TableCreator("Quiz_Header", fields, actions=["Edit"],domain="quizzes/")
    table_creator.set_items_per_page(12)
    table_creator.create_view()
    table = table_creator.create(page_num)
     
    return render_template("quizzes/view_quizzes.html",table=table)
 
@quiz.route("/add_quiz",methods=['GET','POST'])
@admin_required
def add_quiz():
    if request.method=='POST':
        description = request.form['description']
        
        if Quiz_Header.query.filter_by(description=description).first() is not None:
            flash('Quiz already exists')
            return redirect(url_for('quiz.add_quiz'))
        record = {
            "description": description,
            "multiple_retries": False if 'multiple_retries' not in request.form else request.form['multiple_retries'] == 'on',
            "active": False if 'active' not in request.form else request.form['active'] == 'on',
            "grade_category": request.form['grade_category']
        }
        quiz = Quiz_Header(**record)
        db.session.add(quiz)
        db.session.commit()
        return redirect(url_for('quiz.add_quiz_topic',quiz_header_id=quiz.id))
    
    return render_template('quizzes/add_quiz.html')

def topics_table(quiz_header):
    fields = {
        'id': Field(None,None),
        'quiz_header': Field(None,None),
        'topic': Field(None,'Topic'),
        'number_of_questions': Field(None,'No. of Questions')
        
    }

    table_creator = TableCreator("Quiz_Topics", fields, condition=f'quiz_header={quiz_header}',actions=["Edit","Delete"],domain="quiz_topics/")
    table_creator.set_items_per_page(12)
    table_creator.create_view()
    table = table_creator.create(1)
    
    return table

@quiz.route('/quiz_topics/<int:quiz_header_id>')
@admin_required
def quiz_topics(quiz_header_id):
    header = Quiz_Header.query.filter_by(id=quiz_header_id).first()
    if header is None:
        return redirect(url_for('quiz.view_quizzes',page_num=1))
     
    return render_template("quizzes/view_quiz_topics.html",table=topics_table(header.id),quiz_header=header)
    

@quiz.route("/add_quiz_topic/<int:quiz_header_id>")
@admin_required
def add_quiz_topic(quiz_header_id):
   
    return render_template('quizzes/add_quiz_topic.html',topics=Topics(),header_id=quiz_header_id)


@quiz.route('/add_quiz_topic',methods=['POST'])
@admin_required
def add_quiz_topics_post():
    record = {
        'quiz_header': request.form['header_id'],
        'topic': request.form['topic'],
        'number_of_questions': request.form['questions']
    }
    quiz_topics = Quiz_Topics(**record)
    db.session.add(quiz_topics)
    db.session.commit()
    return redirect(url_for('quiz.quiz_topics',quiz_header_id=quiz_topics.quiz_header))

@quiz.route('/quiz_topics/delete/<int:id>')
@admin_required
def del_quiz_topic(id):
    qt = Quiz_Topics.query.filter_by(id=id).first()
    if qt:
        db.session.delete(qt)
        db.session.commit()
    return redirect(url_for('quiz.quiz_topics',quiz_header_id=qt.quiz_header))
        
@quiz.route('/quiz_topics/update/<int:id>')
@admin_required
def update_quiz_topic(id):
    
    qt = Quiz_Topics.query.filter_by(id=id).first()
    return render_template('quizzes/edit_quiz_topic.html',quiz_topic=qt,topics=Topics())

@quiz.route('/quiz_topics/update',methods=['POST'])
@admin_required
def update_quiz_topic_post():
    quiz_header = request.form['header_id']
    topic = request.form['topic']
    qt = Quiz_Topics.query.filter_by(quiz_header=quiz_header,topic=topic).first()
    qt.topic = topic
    qt.number_of_questions = request.form['questions']
    db.session.commit()
    return redirect(url_for('quiz.quiz_topics',quiz_header_id=qt.quiz_header))


@quiz.route("/quizzes/update/<int:id>")
@admin_required
def edit_quiz(id):
    quiz = Quiz_Header.query.filter_by(id=id).first()

    return render_template('quizzes/edit_quiz.html',quiz=quiz,table=topics_table(quiz.id))

@quiz.route("/quizzes/update",methods=['POST'])
@admin_required
def edit_quiz_post():
    quiz = Quiz_Header.query.filter_by(description=request.form['description']).first()    
    
    quiz.grade_category = request.form['grade_category']
    if 'multiple_retries' in request.form:
        quiz.multiple_retries = request.form['multiple_retries'] == 'on'
    else:
        quiz.multiple_retries = False
    if 'active' in request.form:
        quiz.active = request.form['active'] == 'on'
    else:
        quiz.active = False
    db.session.commit()
    
    return redirect(url_for('quiz.view_quizzes',page_num=1))
    
@quiz.route("/quiz_duedate/<int:id>")
@admin_required
def quiz_duedate(id):
    quiz = Quiz_Header.query.filter_by(id=id).first()
    fields = {
        'id': Field(None,None),
        'quiz_header': Field(None,'Quiz Header'),
        'section': Field(None,'Section'),
        'date_due': Field(timestamp_to_date,'Date Due')
    }

    table_creator = TableCreator("Quiz_DueDates", fields, condition=f"quiz_duedates.quiz_header={id}",actions=["Edit"],domain="quiz_due_date/")
    table_creator.set_items_per_page(12)
    table_creator.create_view()
    table = table_creator.create(1)
     
    return render_template("quizzes/quizzesdue.html",table=table,quiz=quiz.id)
    
@quiz.route("/add_quiz_duedate/<int:id>")
@admin_required
def add_quiz_duedate(id):
    quiz = Quiz_Header.query.filter_by(id=id).all()
    sections = Sections.query.all()
    return render_template('quizzes/add_quiz_duedate.html',quizzes=quiz,sections=sections)

@quiz.route("/add_quiz_duedate",methods=['POST'])
@admin_required
def add_quiz_duedate_post():
    record = {
        "quiz_header": request.form['quiz'],
        "section": request.form['sectionid'],
        "date_due": dt.strptime(request.form['duedate'].replace('T',' '),'%Y-%m-%d %H:%M')
    }
    quiz_duedate = Quiz_DueDates(**record)
    db.session.add(quiz_duedate)
    db.session.commit()
    return redirect(url_for('quiz.quiz_duedate',id=request.form['quiz']))


@quiz.route('/generate_quizzes/<int:quiz_header>')
@admin_required
def generate_quizzes(quiz_header):
    stmt = "SELECT user.id FROM user  left join "
    stmt += f"(select quiz_header,user_id from Quizzes where quiz_header = {quiz_header})"
    stmt += "on user.id = user_id where user_id is null"
    
    users = list(db.session.execute(text(stmt)))

    if len(users) == 0:
        return redirect(url_for('quiz.quiz_duedate',id=quiz_header))
    create_quiz_users(quiz_header,users[:10])
    return redirect(url_for('quiz.generate_quizzes',quiz_header=quiz_header))
    
@quiz.route('/student_quizzes/<int:quiz_header>/<int:page_num>')
@admin_required
def student_quizzes(quiz_header,page_num):
    
    fields = {
        'id': Field(None,'Quiz ID'),
        'quiz_header': Field(None,'Quiz Header'),
        'user_id': Field(None,'User ID'),
        'submitted': Field(None,'Submitted'),
        'grade': Field(round_to_2_decimals,'Grade')
        
    }

    table_creator = TableCreator("Quizzes", fields, condition=f"quizzes.quiz_header={quiz_header}",actions=["View"],domain=f"student_quizzes/{quiz_header}/")
    table_creator.set_items_per_page(12)
    table_creator.create_view()
    table = table_creator.create(page_num)
     
    return render_template("quizzes/student_quizzes.html",table=table)
    
