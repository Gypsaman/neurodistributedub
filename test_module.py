from webproject import create_app, db
from webproject.models import QuestionBank,AnswerBank, Questions, Quiz_Topics, Quiz_Header, Quizzes
import json
from webproject import create_app, db

with create_app().app_context():
    qt = Quiz_Topics.query.filter_by(quiz_header=11).first()
    print(qt)



# quizzes = json.load(open('./data/quizzes.json','r'))

# tokens = [question for id,question in quizzes.items() if question['Topic'] == 'Tokens']
# for token in tokens:
#     print(token['Question'])
#     for answer in token['Answers']:
#         print('\t'+answer['Answer'])
#     print('**********************************************************')