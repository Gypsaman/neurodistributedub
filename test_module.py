from webproject.models import User,Quizzes, Questions,Answers, Quiz_DueDates
from webproject import db,create_app
from sqlalchemy import text
from webproject.modules.quizzes import create_quiz_users
from sqlalchemy import text


with create_app().app_context():
    date_due = Quiz_DueDates.query.filter_by(quiz_header=8,section=2).first().date_due
    print(date_due)
    



