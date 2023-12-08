from webproject import create_app, db
from webproject.models import QuestionBank,AnswerBank, Questions, Quiz_Topics, Quiz_Header, Quizzes, Answers
import json
from webproject import create_app, db
from webproject.modules.offline_utils import email_course_evaluation
from graders.check_submissions import check_submissions
from webproject.models import User,Quiz_Header, Quizzes

with create_app().app_context():
    qh = Quiz_Header.query.filter_by(description='Final').first()
    quiz = Quizzes.query.filter_by(quiz_header=qh.id,user_id=127).first()
    print(quiz)

