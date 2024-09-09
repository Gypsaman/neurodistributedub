from webproject import create_app, db
from webproject.models import  Quiz_Header, Quiz_Topics, Assignments, QuestionBank, AnswerBank, Quizzes, Answers, Questions
from graders.check_submissions import check_submissions
from graders.MidTermExam import build_exam_distribution, email_exams
from webproject.modules.create_initial_data import (
    check_user_to_roster,
    create_users_from_roster,
)
from graders.final_grade import publish_final_grades, final_grades_student
from webproject.modules.grading import build_grades
import json
from datetime import datetime as dt
from webproject.modules.grading import course_evaluation_email, publish_final_grades
from webproject.modules.quizzes import create_quiz_users

import os
from sqlalchemy import text

    
def save_data(query, filename):
    with open(os.path.join('./data',filename), 'w') as f:
        f.write('[')
        for item in query:
            f.write(json.dumps(item.to_dict())+',\n')
        f.write('{}]')

# with create_app().app_context():
#     models = [
#         [Assignments.query.all(),'assignments.json'],
#         [Quiz_Header.query.all(),'quiz_header.json'],
#         [Quiz_Topics.query.all(),'quiz_topics.json'],
#         [QuestionBank.query.all(),'question_bank.json'],
#         [AnswerBank.query.all(),'answer_bank.json'],

#     ]
#     for model in models:
#         save_data(model[0], model[1])

# from webproject.models import User,Sections
with create_app().app_context():
    db.create_all()

# from webproject.modules.create_initial_data import create_initial_data

# create_initial_data()