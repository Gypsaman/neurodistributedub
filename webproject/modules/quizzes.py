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

def create_quiz(
    description: str,
    date_available: dt,
    date_due: dt,
    topics: dict,
    multiple_retries: bool=True,
    active: bool=True
    ):
    quiz_header = Quiz_Header(description=description,
                              date_available=date_available,
                              date_due=date_due,
                              multiple_retries=multiple_retries,
                              active=active)
    db.session.add(quiz_header)
    db.session.commit()
    for topic,qty in topics.items():
        quiz_topic = Quiz_Topics(quiz_header=quiz_header.id,
                                 topic=topic,
                                 number_of_questions=qty)
        db.session.add(quiz_topic)
    db.session.commit()
    
    return quiz_header.id
        

def create_quiz_user(quiz_id: int,
                user_id,
                
    ):
    quiz = Quizzes(quiz_header=quiz_id,
                   user_id=user_id, 
                   submitted=False,
                   grade=None)
    db.session.add(quiz)
    db.session.commit()
    topic_count = 0
    for quiz_topic in Quiz_Topics.query.filter_by(quiz_header=quiz_id).all():
        topic = quiz_topic.topic
        qty = quiz_topic.number_of_questions
        selection = np.random.choice(range(1,qty+1),qty ,replace=False).tolist()
        for idx,question in enumerate(QuestionBank.query.filter_by(topic=quiz_topic.topic).all()):
            if (idx+1) not in selection:
                continue
            record = Questions(quiz_id=quiz.id,
                               question_id=question.question_id,
                               topic = topic,
                               question=question.question,
                               display_order=selection.index(idx+1)+topic_count,
                               answer_chosen='',
                               is_correct=False)
            
            db.session.add(record)
            db.session.commit()

            
            answer_count = AnswerBank.query.filter_by(question_id=question.question_id).count()
            answer_selection = np.random.choice(range(1,answer_count+1),answer_count,replace=False).tolist()
            for order,a in enumerate(AnswerBank.query.filter_by(question_id=question.question_id).all()):
                if (order+1) not in answer_selection:
                    continue
                answer = Answers(quiz_id=quiz.id,
                                 question_id=question.question_id,
                                 answer_id=a.answer_id,
                                 display_order=answer_selection.index(order+1),
                                 answer_txt=a.answer_txt,
                                 correct_answer=a.correct_answer)
                db.session.add(answer)
                db.session.commit()
        topic_count += qty
            
    return quiz.id
   
def create_final(topics_selected:dict,StartTime:dt):
    with create_app().app_context():
        users = User.query.all()
        for user in users:
            quiz_id = create_quiz(topics_selected,StartTime,dt.now()+timedelta(hours=2),description='Final for {}'.format(user.first_name),user_id=user.id,multiple_retries=False)
            print('Created quiz {} for {}'.format(quiz_id,user.first_name))
           

def create_quiz_all_users(section_name:str,
                          quiz_header_id:int,silent=True
    ):     
    with create_app().app_context():
        section = Sections.query.filter_by(section=section_name).first()
        users = User.query.filter_by(section=section.id,role='student').all()
        for user in users:
            q = Quizzes.query.filter_by(quiz_header=quiz_header_id,user_id=user.id).first()
            if not q:
                quiz_id = create_quiz_user(quiz_header_id,user.id)
                if not silent:
                    print('Created quiz {} for {}'.format(quiz_id,user.first_name))           

    
def create_quiz_users(quiz_header_id:int,users:list):
    
    for user in users:
        create_quiz_user(quiz_header_id,user[0])


if __name__ == '__main__':
    topics_selected = {"NFT": 11}
    quiz_id = create_quiz(
                description= "NFT Quiz",
                date_available= dt.now(),
                date_due= dt.now()+timedelta(days=7),
                topics = topics_selected,
                multiple_retries=True,
                active=True
                )
    create_quiz_all_users('SP23-Wednesday',quiz_id)

