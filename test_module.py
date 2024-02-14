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

with create_app().app_context():
    # build_exam_distribution()

    # email_exams(section=2)
    for attendance in Attendance.query.filter(Attendance.date > dt.strptime('2024-02-14',"%Y-%m-%d")).all():
        print(attendance)


        


