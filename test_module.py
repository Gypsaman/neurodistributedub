from webproject import create_app,db
from webproject.models import QuestionBank,AnswerBank
from webproject.modules.create_initial_data import create_users_from_roster,create_initial_data
from webproject.modules.quizzes import create_quiz_users
from sqlalchemy import text
import json

quizz_questions = {}
with create_app().app_context():
    for question in QuestionBank.query.all():
        quizz_questions[question.question_id] = {'question':question.question,'topic':question.topic,'answers':[]}
        for answer in AnswerBank.query.filter_by(question_id=question.question_id).all():
            quizz_questions[question.question_id]['answers'].append({'answer_id':answer.answer_id,'answer_txt':answer.answer_txt,'correct_answer':answer.correct_answer})
    json.dump(quizz_questions,open('quizz_questions.json','w'),indent=4)

    
        




