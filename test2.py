from webproject import create_app,db
from webproject.models import Quiz_Header,Assignments, Answers,Questions, Quizzes
from webproject.modules.create_initial_data import create_users_from_roster,create_initial_data
from webproject.modules.quizzes import create_quiz_users
from sqlalchemy import text

with create_app().app_context():

    for quiz in Quizzes.query.all():
        print(quiz)
    for question in Questions.query.all():
        print(question)
    for answer in Answers.query.all():
        print(answer)