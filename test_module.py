from webproject import create_app, db
from webproject.models import User, Submissions, Attendance, Quizzes, Questions,Answers, Quiz_Header
from graders.check_submissions import check_submissions
from graders.MidTermExam import build_exam_distribution, email_exams
from webproject.modules.create_initial_data import (
    check_user_to_roster,
    create_users_from_roster,
)
from graders.final_grade import publish_final_grades, final_grades_student
import json
from datetime import datetime as dt
from webproject.modules.grading import is_this_function_duplicate

with create_app().app_context():
    build_exam_distribution()

    email_exams(section=2)
    # is_this_function_duplicate()


        


