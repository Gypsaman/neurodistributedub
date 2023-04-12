import json
from collections import Counter
import numpy as np
from webproject import create_app, db
from webproject.models import Quizzes, Questions, Answers, User, Sections
from datetime import datetime as dt
from datetime import timedelta

questions = json.load(open('./data/quizzes.json','r'))
Topics = Counter([q['Topic'] for id,q in questions.items()])


def create_quiz(topics_selected,
                date_available,
                date_due,
                description,
                user_id,
                multiple_retries=True
    ):
    quiz = Quizzes(description=description,user_id=user_id, date_available=date_available,date_due=date_due,submitted=False,multiple_retries=multiple_retries)
    db.session.add(quiz)
    db.session.commit()
    question_number = 1
    for topic,qty in topics_selected.items():
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
            break

def create_quiz_all_users(section_name:str,
                          description,
                          topics_selected:dict
    ):     
    with create_app().app_context():
        section = Sections.query.filter_by(section=section_name).first()
        users = User.query.filter_by(section=section.id,role='student').all()
        for user in users:
            quiz_id = create_quiz(topics_selected,dt.now(),dt.now()+timedelta(days=7),description=description + ' for {}'.format(user.first_name),user_id=user.id)
            print('Created quiz {} for {}'.format(quiz_id,user.first_name))           

    
if __name__ == '__main__':
    topics_selected = {"NFT": 11}
    create_quiz_all_users('SP23-Wednesday','NFT',topics_selected)

