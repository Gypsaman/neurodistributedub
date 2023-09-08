from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required,current_user
from webproject.routes import admin_required

from webproject import db
from webproject.models import  User, Wallet, Assets, Assignments, Submissions, Grades, Sections
from webproject.modules.table_creator import Field, TableCreator, timestamp_to_date, only_contract, round_to_2_decimals,round_to_0_decimals
from webproject.modules.web3_interface import get_eth_balance

dashb = Blueprint("dashb", __name__)

submission_page = 1
grades_page = 1

def create_dashboard(user_id,submission_page=1,grades_page=1,quiz_page=1):


    grade_fields = {
        "grades.id": Field(None, None),
        'assignments.name': Field(None, 'Assignment'),
        "dategraded": Field(timestamp_to_date, "Date Submitted"),
        "grade": Field(round_to_0_decimals, "Grade"),
    }
    actions = [] 
    table_creator = TableCreator(
        "Grades", grade_fields, condition=f'user_id = {user_id}', actions=actions
    )
    table_creator.join("Assignments", "Grades.assignment == Assignments.id")
    table_creator.set_items_per_page(10)
    table_creator.domain = f'dashboard?submissions_page={submission_page}&quiz_page={quiz_page}&grades_page='
    table_creator.create_view()
    grades_table = table_creator.create(grades_page)

    quiz_fields = {
        'quiz_header.id': Field(None, None),
        'description': Field(None, 'Description'),
        'date_due': Field(timestamp_to_date, 'Due Date'),
        'Grade': Field(round_to_0_decimals, 'Grade'),
    }
    actions = []
    table_creator = TableCreator("Quiz_Header", quiz_fields, condition=f'active = {True}', actions=actions)
    table_creator.join("Quizzes", f"Quizzes.quiz_header == Quiz_Header.id And Quizzes.user_id == {user_id}")
    table_creator.set_items_per_page(5)
    table_creator.domain = f'dashboard?submissions_page={submission_page}&grades_page={grades_page}&quiz_page='
    table_creator.create_view()
    quiz_table = table_creator.create(quiz_page)


    submission_fields = {
        "assignments.name": Field(None, "Assignment"),
        "submission": Field(only_contract, "Submission"),
        "date_submitted": Field(timestamp_to_date, "Submitted"),
        "grade": Field(None, "Grade")
    }
    actions=[]
    table_creator = TableCreator("Submissions", submission_fields, condition=f"user_id = {user_id}", actions=actions)
    table_creator.join("Assignments", "Submissions.assignment == Assignments.id")
    table_creator.set_items_per_page(15)
    table_creator.domain= f'dashboard?grades_page={grades_page}&&quiz_page={quiz_page}submissions_page='
    table_creator.create_view(order='date_submitted DESC')
    submissions_table = table_creator.create(submission_page)

    user = User.query.filter_by(id=user_id).first()
    section = Sections.query.filter_by(id=user.section).first()
    wallet = Wallet.query.filter_by(user_id=user_id).first()
    ethbalance = get_eth_balance(wallet.wallet) if wallet is not None else 0
    tokens = Assets.query.filter_by(user_id=user_id, asset_type=1).count()
    nfts = Assets.query.filter_by(user_id=user_id, asset_type=2).count()
    assigments_count = Assignments.query.count()
    submissions_count = Submissions.query.filter_by(user_id=user_id).count()
    grades_count= Grades.query.filter_by(user_id=user_id).count()

    return render_template("/dashboard/dashboard.html",
                           grades_table=grades_table,
                           submissions_table=submissions_table,
                           quizzes_table = quiz_table,
                           user=user,
                           section=section,
                           wallet=wallet,
                           ethbalance=ethbalance,
                           tokens=tokens,nfts=nfts,
                           assigments_count=assigments_count,
                           submissions_count=submissions_count,
                           grades_count=grades_count
                           )



@dashb.route("/dashboard")
@login_required
def dashboard():
    
    if request.args.get("submissions_page"):
        submission_page = int(request.args.get("submissions_page"))
    else:
        submission_page = 1
    if request.args.get("grades_page"):
        grades_page = int(request.args.get("grades_page"))          
    else:
        grades_page = 1
    if request.args.get("quiz_page"):
        quiz_page = int(request.args.get("quiz_page"))
    else:
        quiz_page = 1
    
    return create_dashboard(current_user.id,submission_page=submission_page,grades_page=grades_page,quiz_page=quiz_page)

@dashb.route("/dashboard/<string:student_id>")
@admin_required
def dashboard_student(student_id):
    user = User.query.filter_by(student_id=student_id).first()
    if user is None:
        flash("Student not found")
        return redirect(url_for("dashb.dashboard"))
    return create_dashboard(user.id)

# @dashb.route("/dashboard/student", methods=["POST"])
# @admin_required
# def dashboard_student_post():
#     student_id = request.form.get("studentid")

#     user = User.query.filter_by(id=student_id).first()
#     if user is None:
#         flash("Student not found")
#         return redirect(url_for("dashb.dashboard"))
#     return create_dashboard(user.id)



