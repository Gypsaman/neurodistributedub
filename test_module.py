# from webproject.modules.create_initial_data import create_initial_data,send_new_user_email
from webproject.modules.quizzes import create_quiz, create_quiz_all_users
# from webproject.modules.web3_interface import get_eth_balance
from datetime import datetime as dt
# from datetime import timedelta
# from webproject.models import User,Sections,Quiz_Header,Quiz_Topics, Quizzes,Questions, Answers, Wallet
from webproject import db, create_app
from webproject.modules.dotenv_util import load_dotenv
# from webproject.modules.quizzes import Topics
from graders.check_submissions import check_submissions
# import pandas as pd


from graders.MidTermExam import email_exams
email_exams()
exit()

load_dotenv()
# 
check_submissions()

# with create_app().app_context():
#     section = Sections.query.filter_by(section='FA23-Thursday').first()
#     for user in User.query.filter_by(section=section.id).all():
#         wallet = Wallet.query.filter_by(user_id=user.id).first()
#         eth = get_eth_balance(wallet.wallet) if wallet else 0
#         print(f'{user.student_id},{user.first_name},{user.last_name},{wallet.wallet if wallet else ""},{eth}')

# with create_app().app_context():
#     topics_selected = {"Encryption":7,"Blockchain":5,"Solidity": 8}
#     quiz_id = create_quiz(
#                 description= "Midterm Exam",
#                 date_available= dt.strptime('10/13/2023 16:59','%m/%d/%Y %H:%M'),
#                 date_due=dt.strptime('10/13/2023 19:00','%m/%d/%Y %H:%M'),
#                 topics = topics_selected,
#                 multiple_retries=True,
#                 active=True
#                 )
#     create_quiz_all_users('FA23-Monday',quiz_id)