# from webproject.modules.create_initial_data import create_initial_data,send_new_user_email
from webproject.modules.quizzes import create_quiz, create_quiz_all_users
from webproject.modules.web3_interface import get_eth_balance
from datetime import datetime as dt
# from datetime import timedelta
from webproject.models import User,Sections,Quiz_Header,Quiz_DueDates,Quiz_Topics, Quizzes,Questions, Answers, Wallet, Submissions, Assignments
from webproject import db, create_app
from webproject.modules.dotenv_util import load_dotenv
# from webproject.modules.quizzes import Topics
from graders.check_submissions import check_submissions
from graders.final_grade import final_grades_student
from webproject.modules.ubemail import UBEmail

load_dotenv()
check_submissions()

# with create_app().app_context():
#     qh = Quiz_Header.query.filter_by(description='brownie').first()
#     if not qh:
#         print('Header not found')
#         exit()
#     for q in Quizzes.query.filter_by(quiz_header=qh.id).all():
#         print(q)

            



