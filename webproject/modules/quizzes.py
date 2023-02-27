import json
from collections import Counter
import numpy as np
from webproject import create_app, db
from webproject.models import Quizzes, Questions, Answers
from datetime import datetime as dt

questions = json.load(open('./data/quizzes.json','r'))
Topics = Counter([q['Topic'] for id,q in questions.items()])


def create_quiz(topics_selected,date_available,date_due,description,multiple_retries=True):
    quiz = Quizzes(description=description,user_id = 1, date_available=date_available,date_due=date_due,submitted=False,multiple_retries=multiple_retries)
    db.session.add(quiz)
    db.session.commit()
    question_number = 1
    for topic,qty in topics_selected.items():
        selection = np.random.choice(range(Topics[topic]),qty ,replace=False)
        topic_questions = np.array([id for id,q in questions.items() if q['Topic'] == topic])
        for q in topic_questions[selection]:
            question = Questions(quiz_id=quiz.id,question_id=q,question=questions[q]['Question'],display_order=question_number,answer_chosen='',is_correct=False)
            db.session.add(question)
            db.session.commit()
            question_number += 1
            
            answers = np.array(questions[q]['Answers'])
            selection = np.random.choice(range(len(answers)),len(answers),replace=False)
            for order,a in enumerate(answers[selection]):
                answer = Answers(quiz_id=quiz.id,question_id=q,answer_id=a['ID'],display_order=order+1,answer_txt=a['Answer'],correct_answer=a['Correct'])
                db.session.add(answer)
                db.session.commit()
            
    return quiz.id
        

    
if __name__ == '__main__':
    topics_selected = {'Encryption': 5, 'Blockchain': 3,"Solidity": 2}
    quiz_id = create_quiz(topics_selected)
    print(quiz_id)

    quiz = Quizzes.query.filter_by(quiz_id=quiz_id).join(Questions).join(Answers).first()
    print(quiz)
