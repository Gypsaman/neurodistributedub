from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required,current_user

from webproject import db
from webproject.models import  User, Wallet, Assets, Assignments, Submissions, Grades
from webproject.modules.table_creator import Field, TableCreator, timestamp_to_date


dashb = Blueprint("dashb", __name__)

@dashb.route("/dashboard")
@login_required
def dashboard():
    
    grade_fields = {
        "grades.id": Field(None, None),
        'assignments.name': Field(None, 'Assignment'),
        "dategraded": Field(timestamp_to_date, "Date Submitted"),
        "grade": Field(None, "Grade"),
    }
    actions = [] 
    table_creator = TableCreator(
        "Grades", grade_fields, condition=f'user_id = {current_user.id}', actions=actions
    )
    table_creator.join("Assignments", "Grades.assignment == Assignments.id")
    table_creator.set_items_per_page(15)
    table_creator.create_view()
    grades_table = table_creator.create(1)

    submission_fields = {
        "assignments.name": Field(None, "Assignment"),
        "submission": Field(None, "Submission"),
        "date_submitted": Field(timestamp_to_date, "Submitted"),
        "grade": Field(None, "Grade")
    }
    actions=[]
    table_creator = TableCreator("Submissions", submission_fields, condition=f"user_id = {current_user.id}", actions=actions)
    table_creator.join("Assignments", "Submissions.assignment == Assignments.id")
    table_creator.set_items_per_page(35)
    table_creator.create_view()
    submissions_table = table_creator.create(1)

    user = User.query.filter_by(id=current_user.id).first()
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    tokens = Assets.query.filter_by(user_id=current_user.id, asset_type=1).count()
    nfts = Assets.query.filter_by(user_id=current_user.id, asset_type=2).count()
    assigments_count = Assignments.query.count()
    submissions_count = Submissions.query.filter_by(user_id=current_user.id).count()
    grades_count= Grades.query.filter_by(user_id=current_user.id).count()

    return render_template("/dashboard/dashboard.html",
                           grades_table=grades_table,
                           submissions_table=submissions_table,
                           user=user,
                           wallet=wallet,
                           tokens=tokens,nfts=nfts,
                           assigments_count=assigments_count,
                           submissions_count=submissions_count,
                           grades_count=grades_count
                           )
