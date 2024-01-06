from webproject import create_app,db
from webproject.models import QuestionBank,AnswerBank
from webproject.modules.create_initial_data import create_users_from_roster,create_initial_data, create_user_quizzes
from webproject.models import Quizzes, Questions, Answers
from sqlalchemy import text
import json
from webproject.modules.offline_utils import import_quiz_questions

import_quiz_questions()

# with create_app().app_context():
    
#     quiz = Quizzes.query.filter_by(id=48).first()
#     for question in Questions.query.filter_by(quiz_id=quiz.id).order_by(Questions.display_order).all():
#         print(question)
#         for answer in Answers.query.filter_by(question_id=question.question_id).order_by(Answers.display_order).all():
#             print(answer)
#         print('*'*50)
    # create_user_quizzes()
    # for question in QuestionBank.query.all():
    #     print(question)
    #     for answer in AnswerBank.query.filter_by(question_id=question.question_id).all():
    #         print(answer)
    
    
    # for id,question in json.load(open('quizz_questions.json')).items():
    #     question_bank = QuestionBank(topic=question['topic'],question=question['question'])
    #     db.session.add(question_bank)
    #     db.session.commit()
    #     db.session.refresh(question_bank)
    #     for answer in question['answers']:
    #         db.session.add(AnswerBank(question_id=question_bank.question_id,answer_txt=answer['answer_txt'],correct_answer=answer['correct_answer']))
    #         db.session.commit()
            

    
        




