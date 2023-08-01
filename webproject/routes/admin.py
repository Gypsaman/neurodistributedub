from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from webproject import db
from webproject.models import Assignments, DueDates, Grades, Submissions, User, Sections, Quiz_Header, Quiz_Topics
from webproject.modules.table_creator import Field, TableCreator, timestamp_to_date
from webproject.routes import admin_required
from datetime import datetime as dt
from webproject.modules.quizzes import Topics

admin = Blueprint("admin", __name__)


@admin.route("/admin")
@admin_required
def admin_welcome():
    return render_template("admin/admin.html")


@admin.route("/admin/submissionselect")
@admin_required
def submission_select():

    assignments = Assignments.query.all()
    return render_template(
        "admin/admin_submission_select.html",
        assignments=assignments,
        sendto="/admin/submissionselect",
    )


@admin.route("/admin/submissionselect", methods=["POST"])
@admin_required
def submission_select_post():

    assignment = Assignments.query.filter_by(
        id=request.form["assignment"]
    ).first()
    fields = {
        "submissions.id": Field(None, None),
        "user.student_id": Field(None, "Student Id"),
        "submission": Field(None, "Submission"),
        "date_submitted": Field(timestamp_to_date, "Date Submitted"),
        "grade": Field(None, "Grade"),
    }
    actions = ["Delete"] if current_user.role == "admin" else []
    table_creator = TableCreator(
        "Submissions", fields, condition=f"assignment={assignment.id}", actions=actions
    )
    table_creator.join("User", "submissions.user_id == User.id")
    table_creator.set_items_per_page(55)
    table_creator.create_view()
    table = table_creator.create(1)

    return render_template(
        "admin/admin_submissions.html", assignment=assignment, table=table
    )


@admin.route("/submissions/delete/<int:id>")
@admin_required
def del_submissions(id):
    submission = Submissions.query.filter_by(id=id).first()
    db.session.delete(submission)
    db.session.commit()
    return redirect(url_for("admin.submission_select"))


@admin.route("/admin/assignmentsdue")
@admin_required
def assigmentsdue():
    assignments = Assignments.query.all()
    return render_template(
        "admin/admin_submission_select.html",
        assignments=assignments,
        sendto="/admin/assignmentsdue",
    )


@admin.route("/admin/assignmentsdue", methods=["POST"])
@admin_required
def assigmentsdue_post():
    assignment = request.form["assignment"]

    fields = {
        "due_dates.id": Field(None, None),
        "assignments.name": Field(None, "Assignment"),
        "section": Field(None, "Section"),
        "duedate": Field(timestamp_to_date, "Due Date"),
    }
    actions = ["Edit", "Delete"]
    table_creator = TableCreator("Due_Dates", fields, condition=f"due_dates.assignment={assignment}",actions=actions)
    table_creator.set_items_per_page(15)
    table_creator.join("Assignments", "assignments.id=due_dates.assignment")
    table_creator.create_view()
    table = table_creator.create(1)
    return render_template("admin/assignmentsdue.html", table=table,assignment=assignment)


@admin.route('/addduedate/<int:id>')
@admin_required
def add_duedate(id):
    assignments = Assignments.query.all()
    sections = Sections.query.all()
    return render_template('admin/addduedate.html', assignments=assignments,selected=id,sections=sections)

@admin.route('/addduedate', methods=['POST'])
@admin_required
def add_duedate_post():
    record = {
        'assignment': request.form['assignment'],
        'section': request.form['sectionid'],
        'duedate': dt.strptime(request.form['duedate'].replace('T',' '),'%Y-%m-%d %H:%M')
    }
    duedate = DueDates(**record)
    db.session.add(duedate)
    db.session.commit()
    return redirect(url_for('admin.assigmentsdue'))


@admin.route("/grades/delete/<int:id>")
@admin_required
def grades_del(id):
    grade = Grades.query.filter_by(id=id).first()
    db.session.delete(grade)
    db.session.commit()

    return redirect(url_for("admin.grades_select"))

@admin.route("/admin/gradesselect")
@admin_required
def grades_select():

    assignments = Assignments.query.all()
    return render_template(
        "admin/admin_submission_select.html",
        assignments=assignments,
        sendto="/admin/gradesselect",
    )


@admin.route("/admin/gradesselect", methods=["POST"])
@admin_required
def grades_select_post():

    assignment = Assignments.query.filter_by(
        id=request.form["assignment"]
    ).first()
    fields = {
        "grades.id": Field(None, None),
        "user.student_id": Field(None, "Student Id"),
        "dategraded": Field(timestamp_to_date, "Date Submitted"),
        "grade": Field(None, "Grade"),
    }
    actions = ["Delete"] if current_user.role == "admin" else []
    table_creator = TableCreator(
        "Grades", fields, condition=f"assignment={assignment.id}", actions=actions
    )
    table_creator.join("User", "grades.user_id == User.id")
    table_creator.set_items_per_page(15)
    table_creator.create_view()
    table = table_creator.create(1)

    return render_template(
        "admin/admin_submissions.html", assignment=assignment, table=table
    )


@admin.route("/admin/user/<int:page_num>")
@admin_required
def users(page_num):

    users = User.query.all()
    fields = {
        "user.id": Field(None, None),
        "first_name": Field(None, "First Name"),
        "last_name": Field(None, "Last Name"),
        "email": Field(None, "Email"),
        "student_id": Field(None, "Student ID"),
        "sections.section": Field(None, "Section"),
        "role": Field(None, "Role"),
    }

    table_creator = TableCreator("User", fields, actions=["Edit"],domain="/admin/user/")
    table_creator.join("Sections", "user.section == Sections.id")
    table_creator.set_items_per_page(12)
    table_creator.create_view()
    table = table_creator.create(page_num)
    return render_template("admin/users.html", table=table,users=users)

@admin.route("/admin/grade-history/<string:section>")
def grade_history_section(section):
    return redirect(url_for('admin.grade_history',section=section,page=1))

@admin.route("/admin/grade-history/<string:section>/<int:page>")
def grade_history(section,page):
    
    import pandas as pd
    from webproject.modules import offline_utils as ou
    df = ou.grade_history_data(section)
    table = TableCreator('Grade History',fields={},actions=[],domain='/admin/grade-history/'+section+'/')
    table.dataframe(df,index=['Student ID'])
    table.set_items_per_page(15)
    html = table.create(page)
    return render_template('admin/grade_history.html',table=html,section=section)
             
@admin.route("/admin/quizzes",methods=['GET','POST'])
def quizzes():
    if request.method=='POST':
        description = request.form['description']
        if Quiz_Header.query.filter_by(description=description).first() is not None:
            flash('Quiz already exists')
            return redirect(url_for('admin.quizzes'))
        record = {
            "description": description,
            "date_available": request.form['date_available'],
            "date_due" : request.form['date_due'],
            "multiple_retries": request.form['multiple_retries'] == 'on',
            "active": request.form['active'] == 'on'
        }
        quiz = Quiz_Header(**record)
        db.session.add(quiz)
        return redirect(url_for('admin.add_quiz_topics',id=quiz.id))
    
    return render_template('quizzes/add_quiz.html')

@admin.route("/admin/add-quiz-topics/<int:id>",methods=['GET','POST'])
def add_quiz_topics(quiz_header_id):
    if request.method=='POST':
        record = {}
        quiz_topics = Quiz_Topics(**record)
        db.session.add(quiz_topics)
        return render_template('admin.add_quiz_topics',quiz_header_id=quiz_header_id)
    
    return render_template('admin/add_quiz_topics.html',quiz_header_id=quiz_header_id)

