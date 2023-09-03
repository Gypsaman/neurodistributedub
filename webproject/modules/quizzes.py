import json
from collections import Counter
import numpy as np
from webproject import create_app, db
from webproject.models import Quizzes, Questions, Answers, User, Sections, Quiz_Header, Quiz_Topics
from datetime import datetime as dt
from datetime import timedelta
from webproject.modules.dotenv_util import get_cwd
import os

cwd = get_cwd()
questions = json.load(open(os.path.join(cwd,'data/quizzes.json'),'r'))
Topics = Counter([q['Topic'] for id,q in questions.items()])

def select_topics_final():
    questions = sum([val for key,val in Topics.items()])
    perc = 60/questions
    total = 0
    topic_selected = {}
    for key,val in Topics.items():
        qty = round(val*perc)
        topic_selected[key] = qty
        total += qty
    if total > 60:
        topic_selected['Brownie'] -= 1
    return topic_selected

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
    question_number = 1
    for quiz_topic in Quiz_Topics.query.filter_by(quiz_header=quiz_id).all():
        topic = quiz_topic.topic
        qty = quiz_topic.number_of_questions
        selection = np.random.choice(range(Topics[topic]),qty ,replace=False)
        topic_questions = np.array([id for id,q in questions.items() if q['Topic'] == topic])
        for q in topic_questions[selection]:
            question = Questions(quiz_id=quiz.id,question_id=q,topic=topic,question=questions[q]['Question'],display_order=question_number,answer_chosen='',is_correct=False)
            db.session.add(question)
            db.session.commit()
            question_number += 1
            
            answers = np.array(questions[q]['Answers'])
            answer_selection = np.random.choice(range(len(answers)),len(answers),replace=False)
            for order,a in enumerate(answers[answer_selection]):
                answer = Answers(quiz_id=quiz.id,question_id=q,answer_id=a['ID'],display_order=order+1,answer_txt=a['Answer'],correct_answer=a['Correct'])
                db.session.add(answer)
                db.session.commit()
            
    return quiz.id
   
def create_final(topics_selected:dict,StartTime:dt):
    with create_app().app_context():
        users = User.query.all()
        for user in users:
            quiz_id = create_quiz(topics_selected,StartTime,dt.now()+timedelta(hours=2),description='Final for {}'.format(user.first_name),user_id=user.id,multiple_retries=False)
            print('Created quiz {} for {}'.format(quiz_id,user.first_name))
           

def create_quiz_all_users(section_name:str,
                          quiz_id:int,
    ):     
    with create_app().app_context():
        section = Sections.query.filter_by(section=section_name).first()
        users = User.query.filter_by(section=section.id,role='student').all()
        for user in users:
            quiz_id = create_quiz_user(quiz_id,user.id)
            print('Created quiz {} for {}'.format(quiz_id,user.first_name))           

    
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

