
from webproject.modules.quizzes import create_quiz, Topics
from webproject.models import Quizzes, Questions, Answers, Submissions, User, Assignments
from webproject import create_app, db
from datetime import datetime as dt
from graders.check_submissions import check_submissions
import json
from collections import Counter

check_submissions()
exit()

print(Topics)

with create_app().app_context():

    # topics_selected = {'Web3': 15}
    # description = "Web3 Quiz"
    # quiz_id = create_quiz(topics_selected,description=description,date_available=dt.strptime("2023-02-24","%Y-%m-%d"),date_due=dt.strptime("2020-01-01","%Y-%m-%d"),multiple_retries=True)
    # print(quiz_id)

  
    quizzes = Quizzes.query.filter_by(id=8).all()
    for quiz in quizzes:
        print(f'{quiz.id}-{quiz.description},{quiz.date_available},{quiz.date_due},{quiz.grade}')
        questions = Questions.query.filter_by(quiz_id=quiz.id).order_by(Questions.display_order).all()
        for question in questions:
            print(f'\t{question.display_order}-{question.question},{question.answer_chosen},{question.is_correct}')
            answers = Answers.query.filter_by(quiz_id=quiz.id,question_id=question.question_id).order_by(Answers.display_order).all()
            for answer in answers:
                print("\t\t",answer.display_order,answer.answer_txt,answer.correct_answer)
            print('*'*50)
