from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from webproject import db
from webproject.models import Assignments, DueDates, Grades, Submissions, User, Sections, Quiz_Header, Quiz_Topics
from webproject.modules.table_creator import Field, TableCreator, timestamp_to_date
from webproject.routes import admin_required
from datetime import datetime as dt
from webproject.modules.quizzes import Topics
from webproject.modules.logger import LogType, Log
import os

admin = Blueprint("admin", __name__)


@admin.route("/admin")
@admin_required
def admin_welcome():
    return render_template("admin/admin.html")

@admin.route("/admin/cwd")
@admin_required
def show_cwd():
    current_dir = os.path.dirname(os.path.join(os.path.abspath(__file__),'static/classdocs'))
    cwd = os.listdir(current_dir)
    return render_template("admin/cwd.html",cwd=cwd[0])

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
    assignment_id = request.form["assignment"]
    return redirect(url_for('admin.assignment_view',
                            assignment_id=assignment_id,
                            page_num=1))


@admin.route("/admin/submissions/<int:assignment_id>/<int:page_num>")
@admin_required
def assignment_view(assignment_id,page_num):
    assignment = Assignments.query.filter_by(
        id=assignment_id
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
        "Submissions", 
        fields, 
        condition=f"assignment={assignment.id}", 
        actions=actions,
        domain=f'/admin/submissions/{assignment_id}/'
    )
    table_creator.join("User", "submissions.user_id == User.id")
    table_creator.set_items_per_page(55)
    table_creator.create_view()
    table = table_creator.create(page_num)

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


# @admin.route("/admin/assignmentsdue")
# @admin_required
# def assigmentsdue():
#     assignments = Assignments.query.all()
#     return render_template(
#         "admin/admin_submission_select.html",
#         assignments=assignments,
#         sendto="/admin/assignmentsdue",
#     )


# @admin.route("/admin/assignmentsdue", methods=["POST"])
# @admin_required
# def assigmentsdue_post():
#     assignment = request.form["assignment"]

#     fields = {
#         "due_dates.id": Field(None, None),
#         "assignments.name": Field(None, "Assignment"),
#         "section": Field(None, "Section"),
#         "duedate": Field(timestamp_to_date, "Due Date"),
#     }
#     actions = ["Edit", "Delete"]
#     table_creator = TableCreator("Due_Dates", fields, condition=f"due_dates.assignment={assignment}",actions=actions)
#     table_creator.set_items_per_page(15)
#     table_creator.join("Assignments", "assignments.id=due_dates.assignment")
#     table_creator.create_view()
#     table = table_creator.create(1)
#     return render_template("admin/assignmentsdue.html", table=table,assignment=assignment)




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

    table_creator = TableCreator("User", fields, actions=["Edit"],domain="admin/user/")
    table_creator.join("Sections", "user.section == Sections.id")
    table_creator.set_items_per_page(12)
    table_creator.create_view()
    table = table_creator.create(page_num)
    return render_template("admin/users.html", table=table,users=users)


@admin.route("/admin/user/update/<int:id>")
@admin_required
def user_update(id):
    user = User.query.filter_by(id=id).first()
    sections = Sections.query.all()
    return render_template("admin/user_update.html", user=user,sections=sections,count=len(sections))

@admin.route("/admin/user/update/<int:id>",methods=['POST'])
@admin_required
def user_update_post(id):
    user = User.query.filter_by(id=id).first()
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.email = request.form['email']
    user.student_id = request.form['student_id']
    user.section = request.form['section']
    user.role = request.form['role']
    db.session.commit()
    return redirect(url_for('admin.users',page_num=1))

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

