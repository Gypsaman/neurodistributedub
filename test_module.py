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
# check_submissions()
# 1 id: 1 description: Encryption date available: 2023-09-18 23:59:00 date due 2023-09-24 23:59:00 multiple retires True active True
# 2 id: 2 description: Encryption date available: 2023-09-18 23:59:00 date due 2023-09-24 23:59:00 multiple retires True active True
# 3 id: 3 description: BlockChain date available: 2023-09-18 23:59:00 date due 2023-09-24 23:59:00 multiple retires True active True
# 4 id: 4 description: BlockChain date available: 2023-09-18 23:59:00 date due 2023-09-24 23:59:00 multiple retires True active True
# 5 id: 5 description: Solidity date available: 2023-10-05 23:59:00 date due 2023-10-12 23:59:00 multiple retires True active True
# 6 id: 6 description: Solidity date available: 2023-10-05 23:59:00 date due 2023-10-12 23:59:00 multiple retires True active True
# 7 id: 7 description: Midterm Exam date available: 2023-10-13 17:00:00 date due 2023-10-13 19:05:00 multiple retires False active True


due_dates= {1:dt(2023,9,24,23,59,0),2:dt(2023,9,24,23,59,0),3:dt(2023,9,24,23,59,0),4:dt(2023,9,24,23,59,0),5:dt(2023,10,12,23,59,0),6:dt(2023,10,12,23,59,0),7:dt(2023,10,13,19,5,0)}
sections = {1:1,2:2,3:1,4:2,5:1,6:2,7:1}
with create_app().app_context():

    for qt in Quiz_Topics.query.all():
        if qt.quiz_header == 2:
            qt.quiz_header = 1
        if qt.quiz_header == 4:
            qt.quiz_header = 3
        if qt.quiz_header == 6:
            qt.quiz_header = 5
    db.session.commit()
    for q in Quizzes.query.all():
        if q.quiz_header == 2:
            q.quiz_header = 1
        if q.quiz_header == 4:
            q.quiz_header = 3
        if q.quiz_header == 6:
            q.quiz_header = 5
    db.session.commit()
    for qh in Quiz_Header.query.all():
        if qh.id in [1,3,5,7]:
            due = Quiz_DueDates(quiz_header=qh.id,section=sections[qh.id],date_due=due_dates[qh.id])
            db.session.add(due)
        else:
            db.session.delete(qh)
    db.session.commit()
            



