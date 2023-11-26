from webproject import create_app, db
from webproject.models import QuestionBank,AnswerBank, Questions, Quiz_Topics, Quiz_Header, Quizzes, Answers
import json
from webproject import create_app, db

with create_app().app_context():
    
    # for Question in QuestionBank.query.filter_by(topic='NFT').all():
    #     print(Question)
    #     for answer in AnswerBank.query.filter_by(question_id=Question.question_id).all():
    #         print(answer)
    #     print('**********************************************************')
        
    qh = Quiz_Header.query.filter_by(description='Tokens').first()
    for quiz in Quizzes.query.filter_by(quiz_header=qh.id).all():    
        for question in Questions.query.filter_by(quiz_id=quiz.id).all():
            for answer in Answers.query.filter_by(quiz_id=quiz.id,question_id=question.question_id).all():
                db.session.delete(answer)
            db.session.delete(question)
        db.session.delete(quiz)
    db.session.commit()


# quizzes = json.load(open('./data/quizzes.json','r'))

# tokens = [question for id,question in quizzes.items() if question['Topic'] == 'Tokens']
# for token in tokens:
#     print(token['Question'])
#     for answer in token['Answers']:
#         print('\t'+answer['Answer'])
#     print('**********************************************************')