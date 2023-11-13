from webproject import create_app, db
from webproject.models import QuestionBank,AnswerBank, Questions
import json



quizzes = json.load(open('./data/quizzes.json','r'))

tokens = [question for id,question in quizzes.items() if question['Topic'] == 'Tokens']
for token in tokens:
    print(token['Question'])
    for answer in token['Answers']:
        print('\t'+answer['Answer'])
    print('**********************************************************')