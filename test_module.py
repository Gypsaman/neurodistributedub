from webproject.models import User,Quizzes, Quiz_Header, Questions,Answers, Quiz_DueDates
from webproject import db,create_app
from sqlalchemy import text
from webproject.modules.quizzes import create_quiz_users
from sqlalchemy import text
from webproject.routes.grades import get_letter_grade


# get_letter_grade()

with create_app().app_context():
    for header in Quiz_Header.query.all():
        print(header.grade_category)
    



