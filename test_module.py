from webproject.modules.create_initial_data import create_initial_data,send_new_user_email
from webproject.modules.quizzes import create_quiz, create_quiz_all_users
from webproject.modules.web3_interface import get_eth_balance
from datetime import datetime as dt
from datetime import timedelta
from webproject.models import User,Sections,Quiz_Header,Quiz_Topics, Quizzes,Questions, Answers, Wallet
from webproject import db, create_app
from webproject.modules.dotenv_util import load_dotenv
from webproject.modules.quizzes import Topics
from graders.check_submissions import check_submissions
import pandas as pd




load_dotenv()

with create_app().app_context():
    section = Sections.query.filter_by(section='FA23-Thursday').first()
    for user in User.query.filter_by(section=section.id).all():
        wallet = Wallet.query.filter_by(user_id=user.id).first()
        eth = get_eth_balance(wallet.wallet) if wallet else 0
        print(f'{user.student_id},{user.first_name},{user.last_name},{wallet.wallet if wallet else ""},{eth}')


