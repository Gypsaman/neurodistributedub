from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required,current_user

from webproject import db
from webproject.models import Assignments, Grades, Submissions, User
from webproject.modules.table_creator import Field, TableCreator, timestamp_to_date
from webproject.routes import admin_required

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
        sendto='/admin/submissionselect'
    )
    
@admin.route("/admin/submissionselect", methods=["POST"])
@admin_required
def submission_select_post():

    assignment = Assignments.query.filter_by(
        name=request.form["assignmentName"]
    ).first()
    fields = {
        "submissions.id": Field(None, None),
        "user.student_id": Field(None, "Student Id"),
        "submission": Field(None, "Submission"),
        "date_submitted": Field(timestamp_to_date, "Date Submitted"),
        "grade": Field(None, "Grade"),
    }
    actions = ['Delete'] if current_user.role=='admin' else []
    table_creator = TableCreator(
        "Submissions", fields, condition=f"assignment={assignment.id}", actions=actions
    )
    table_creator.join("User", "submissions.user_id == User.id")
    table_creator.set_items_per_page(15)
    table_creator.create_view()
    table = table_creator.create(1)

    return render_template(
        "admin/admin_submissions.html", assignment=assignment, table=table
    )

@admin.route('/submissions/delete/<int:id>')
@admin_required
def del_submissions(id):
    submission = Submissions.query.filter_by(id=id).first()
    db.session.delete(submission)
    db.session.commit()
    return redirect(url_for('admin.submission_select'))

@admin.route("/admin/gradesselect")
@admin_required
def grades_select():

    assignments = Assignments.query.all()
    return render_template(
        "admin/admin_submission_select.html", 
        assignments=assignments,
        sendto='/admin/gradesselect'
    )
    
@admin.route('/grades/delete/<int:id>')
@admin_required
def grades_del(id):
    grade = Grades.query.filter_by(id=id).first()
    db.session.delete(grade)
    db.session.commit()
    
    return redirect(url_for('admin.grades_select'))
@admin.route("/admin/gradesselect", methods=["POST"])
@admin_required
def grades_select_post():

    assignment = Assignments.query.filter_by(
        name=request.form["assignmentName"]
    ).first()
    fields = {
        "grades.id": Field(None, None),
        "user.student_id": Field(None, "Student Id"),
        "dategraded": Field(timestamp_to_date, "Date Submitted"),
        "grade": Field(None, "Grade"),
    }
    actions = ['Delete'] if current_user.role=='admin' else []
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


@admin.route('/admin/users/<int:page_num>')
@admin_required
def users(page_num):
    
    fields = {
        'id': Field(None,None),
        'first_name': Field(None,'First Name'),
        'last_name': Field(None,'Last Name'),
        'email': Field(None,'Email'),
        'student_id': Field(None,'Student ID'),
        'role': Field(None,'Role'),

    }
    
    table_creator = TableCreator('User',fields,actions=['Edit','Delete'])
    table_creator.set_items_per_page(30)
    table_creator.create_view()
    table = table_creator.create(page_num)
    return render_template('admin/users.html',table=table)
