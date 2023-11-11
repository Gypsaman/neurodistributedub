from webproject import create_app, db
from webproject.models import QuestionBank,AnswerBank, Questions
import json


quizzes = json.load(open('./data/quizzes.json','r'))



with create_app().app_context():
    for answer in AnswerBank.query.all():
        db.session.delete(answer)
    for question in QuestionBank.query.all():
        db.session.delete(question)
    db.session.commit()

with create_app().app_context():

    for question_number,question in quizzes.items():
            
        question_id = question_number
        topic = question['Topic']
        question_txt = question['Question']
        db.session.add(QuestionBank(question_id=question_id,topic=topic,question=question_txt))
        for answer in question['Answers']:
            answer_id = answer['ID']
            answer_txt = answer['Answer']
            correct_answer = answer['Correct']
            db.session.add(
                AnswerBank(
                    question_id=question_id,
                    answer_id=answer_id,
                    answer_txt=answer_txt,
                    correct_answer=correct_answer)
                )
    db.session.commit()
    print('Done')
