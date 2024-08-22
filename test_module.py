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


with create_app().app_context():
    # for q in Quizzes.query.all():
    #     print(q.to_dict())
    # for q in Questions.query.all():
    #     print(q.to_dict())
    # quiz = Quizzes.query.filter_by(id=2).first()
    # all_questions = Questions.query.filter_by(quiz_id=quiz.id).all()
    # question = Questions.query.filter_by(quiz_id=quiz.id,display_order=1).first()

    # answers = Answers.query.filter_by(question_id=question.question_id).order_by(Answers.display_order).all()
    # print(answers)
    # quiz_header = 2
    # stmt = "SELECT user.id FROM user  left join "
    # stmt += f"(select quiz_header,user_id from Quizzes where quiz_header = {quiz_header})"
    # stmt += "on user.id = user_id where user_id is null"
    
    # users = list(db.session.execute(text(stmt)))
    # create_quiz_users(2,users)
#     print(len(users))
    db.create_all()

from webproject.modules.create_initial_data import create_initial_data

create_initial_data()