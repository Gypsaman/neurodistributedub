import json
from collections import Counter
import numpy as np
from webproject import create_app, db
from webproject.models import Quizzes, Questions, Answers, User, Sections, Quiz_Header, Quiz_Topics, AnswerBank, QuestionBank
from datetime import datetime as dt
from datetime import timedelta
from webproject.modules.dotenv_util import get_cwd
import os

cwd = get_cwd()

def Topics():
    topics = {}
    with create_app().app_context():
        for q in QuestionBank.query.with_entities(QuestionBank.topic,db.func.count(QuestionBank.topic)).group_by(QuestionBank.topic).all():
            topics[q[0]] = q[1]
    return topics

def create_quiz_user(quiz_id: int,
                user_id,
                
    ):
    quiz = Quizzes(quiz_header=quiz_id,
                   user_id=user_id, 
                   submitted=False,
                   grade=None)
    db.session.add(quiz)
    db.session.commit()
    topic_count = 1
    for quiz_topic in Quiz_Topics.query.filter_by(quiz_header=quiz_id).all():
        topic = quiz_topic.topic
        qty = quiz_topic.number_of_questions
        selection = np.random.choice(range(1,qty+1),qty ,replace=False).tolist()
        for idx,question in enumerate(QuestionBank.query.filter_by(topic=quiz_topic.topic).all()):
            if (idx+1) not in selection:
                continue
            record = Questions(quiz_id=quiz.id,
                               topic = topic,
                               question=question.question,
                               display_order=selection.index(idx+1)+topic_count,
                               answer_chosen=0,
                               is_correct=False)
            
            db.session.add(record)
            db.session.commit()
            db.session.refresh(record)

            
            answer_count = AnswerBank.query.filter_by(question_id=question.question_id).count()
            answer_selection = np.random.choice(range(1,answer_count+1),answer_count,replace=False).tolist()
            for order,a in enumerate(AnswerBank.query.filter_by(question_id=question.question_id).all()):
                if (order+1) not in answer_selection:
                    continue
                answer = Answers(question_id=record.question_id,
                                 display_order=answer_selection.index(order+1),
                                 answer_txt=a.answer_txt,
                                 correct_answer=a.correct_answer)
                db.session.add(answer)
                db.session.commit()
        topic_count += qty
            
    return quiz.id

def create_quiz_users(quiz_header_id:int,users:list):
    
    for user in users:
        create_quiz_user(quiz_header_id,user[0])




if __name__ == '__main__':
    pass

