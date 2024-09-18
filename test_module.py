from webproject import create_app, db
from webproject.models import  Quiz_Header, Quiz_Topics, Assignments, QuestionBank, AnswerBank, Quizzes, Answers, Questions, User
# from graders.check_submissions import check_submissions
# from graders.MidTermExam import build_exam_distribution, email_exams
# from webproject.modules.create_initial_data import (
#     check_user_to_roster,
#     create_users_from_roster,
# )
# from graders.final_grade import publish_final_grades, final_grades_student
# from webproject.modules.grading import build_grades
# import json
# from datetime import datetime as dt
# from webproject.modules.grading import course_evaluation_email, publish_final_grades
# from webproject.modules.quizzes import create_quiz_users

# import os
# from sqlalchemy import text
# from graders.check_submissions import check_submissions
    

with create_app().app_context():
    user = User.query.filter_by(email='kdodda@my.bridgeport.edu').first()
    print(user)
    qh = Quiz_Header.query.filter_by(description='Encryption').first()
    print(qh)
    quiz = Quizzes.query.filter_by(quiz_header=qh.id,user_id=user.id).first()
    print(quiz)
    quiz.grade = 100
    db.session.commit()
    


