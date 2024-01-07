from webproject import create_app,db
from webproject.models import QuestionBank,AnswerBank
from webproject.modules.create_initial_data import create_users_from_roster,create_initial_data, create_user_quizzes
from webproject.models import Quizzes, Questions, Answers,Quiz_Header
from sqlalchemy import text
import json
from webproject.modules.offline_utils import import_quiz_questions

with create_app().app_context():
    
    # stmt = "SELECT quiz_header.multiple_retries, quiz_header.description, quizzes.id "
    # stmt += "from quiz_header INNER JOIN quizzes ON quiz_header.id = quizzes.quiz_header "
    # stmt += "INNER JOIN quiz_duedates on quiz_header.id = quiz_duedates.quiz_header and quiz_duedates.section = 1 "
    # stmt += "WHERE quizzes.user_id = 1 and quiz_header.active = 1 "
    # stmt += "ORDER BY quiz_duedates.date_due ASC"

    # quizzes = [{'multiple_retries':mr,'description':desc,'quiz_id':qid} for mr,desc,qid in db.session.execute(text(stmt))]
    # print(quizzes)
    quiz = Quizzes.query.filter_by(id=480).first()
    for question in Questions.query.filter_by(quiz_id=quiz.id).all():
        print(question.answer_chosen)
        

    
    

    




