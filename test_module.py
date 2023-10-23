# from webproject.modules.create_initial_data import create_initial_data,send_new_user_email
from webproject.modules.quizzes import create_quiz, create_quiz_all_users
from webproject.modules.web3_interface import get_eth_balance
from datetime import datetime as dt
# from datetime import timedelta
from webproject.models import User,Sections,Quiz_Header,Quiz_Topics, Quizzes,Questions, Answers, Wallet, Submissions, Assignments
from webproject import db, create_app
from webproject.modules.dotenv_util import load_dotenv
# from webproject.modules.quizzes import Topics
from graders.check_submissions import check_submissions
from graders.final_grade import final_grades_student
from webproject.modules.ubemail import UBEmail

# import pandas as pd

# from graders.imports.SHAIMPORT import SHA256
# hash = SHA256('Cesar')

# from graders.MidTermExam import email_exams
# email_exams()
# exit()
with create_app().app_context():
    for assignment in Assignments.query.all():
        assignment.name = assignment.name.strip()
        print(assignment.id,assignment.name)
    db.session.commit()

exam_students = ["1184077","1187195","1170399","1172542","1172552","1197727","1167056","1198498","1188604"]
with create_app().app_context():
    for user in User.query.all():
        assignment = Assignments.query.filter_by(name='Mid Term 2').first()
        if user.student_id not in exam_students:
            continue
        for submission in Submissions.query.filter_by(user_id=user.id,assignment=assignment.id).all():
            print(user.student_id,submission.grade,submission.comment)
            print('-----------------------------------')
exit()
load_dotenv()
# check_submissions()

# with create_app().app_context():
#     wallet = Wallet.query.filter_by(wallet='0x5c4e0578d1bb46322906df7fcd444cdf00e0f50a').first()
#     if wallet:
#         user = User.query.filter_by(id=wallet.user_id).first()
#         print(user.student_id,user.first_name,user.last_name,user.email)
# # 

# with create_app().app_context():
    
#     for user in User.query.filter_by(role='student').all():
#         wallet = Wallet.query.filter_by(user_id=user.id).first()
#         eth = get_eth_balance(wallet.wallet) if wallet else 0
#         if eth == 0:
#             email = UBEmail()
#             body = f'{user.first_name},\n\nYour wallet is not setup. You will not be able to take the mid term exam programming portion without a wallet.'
#             email.send_email(user.email,f'Wallet Missing',body)
#             print(f'{user.student_id},{user.first_name},{user.last_name},{wallet.wallet if wallet else ""},{eth}')

import json

with create_app().app_context():
        
    for assgn in Assignments.query.all():
            assgn.name = assgn.name.strip()
    db.session.commit()
    all_students = {}

    for user in User.query.filter_by(role='student').all():
        print(user)
        final_grades = final_grades_student(user.id)
        final_grades['email']   = user.email
        final_grades['section'] = user.section
        wallet = Wallet.query.filter_by(user_id=user.id).first()
        final_grades['wallet'] = wallet.wallet if wallet else ""
        
            
        all_students[user.student_id] = final_grades
        
    json.dump(all_students,open('summary.json','w'),indent=4)

all_students = json.load(open('summary.json','r'))    
columns = ['Mid Term','Mid Term 2','Midterm Exam','SHA256','ECC Curve','Wallet','PayUB','myID','Encryption','BlockChain','Solidity']


with open('zero_midterms_details.csv','w') as f:
    
    header = 'section,Student ID,email,wallet'
    for col in columns:
        header += f',{col}'
    f.write(f'{header}\n')
    for student_id,student in all_students.items():
        data =  f"{student['section']},{student_id},{student['email']},{student['wallet']}"
        for col in columns[:3]:
            data += ','
            data += str(student['Midterms'][col]['score']) if col in student['Midterms'] else ''
        for col in columns[3:]:
            data += ','
            data += str(student['Assignments'][col]['score']) if col in student['Assignments'] else ''
        data += '\n'
        f.write(data)
                    
                    
# not_included = ['1069829','1172523','1213915','1212697','1182733','1172732']
# thursday_exam = ['1204936','1205524','1173160','1183157','1163460','1171150','1199689','1207754','1163967']   
# add_email = ['1069829','1182367','1172523','1171150','1188604']
# students_redo = ['1069829','1166843','1167056','1170399','1172523','1172732','1182733','1187195','1188604','1197727','1198498','1212697','1213915','1172542','1184077','1172552']                 

# with open('zero_midterms_details.csv','r') as f:
#     data = f.readlines()
#     for line in data[2:]:
#         line = line.split(',')
#         if line[0] not in thursday_exam:
#                 continue
#         email = UBEmail()
#         body = '''
# The exam will be held via zoom during Thursday's class.

# https://bridgeport.zoom.us/j/93641513602

# At the beggining of class we will go over questions regarding normal class.  After this we will redo the mid term exam.

# During the midterm, you will need to have your VIDEO ON AT ALL TIMES.

# If someone turns off their video or is seen talking with someone else, they will be receive a zero for the exam.

# There were a few students from Monday's class that got booted out of zoom and received a 0.

# '''
        # body = '''
        # A lot of people have been submitting contracts created from a wallet not registered in DNA or have submitted and invalid contract address.
        
        # Please watch this video for training on how to submit, it's only 5 min long.
        
        # https://youtu.be/qZTnU0PtYTE

        
        # '''
        # email.send_email(line[1],'Mid Term Exam - Redo',body)

    
# with create_app().app_context():
#     topics_selected = {"Encryption":7,"Blockchain":5,"Solidity": 8}
#     quiz_id = create_quiz(
#                 description= "Midterm Exam",
#                 date_available= dt.strptime('10/13/2023 17:00','%m/%d/%Y %H:%M'),
#                 date_due=dt.strptime('10/13/2023 19:05','%m/%d/%Y %H:%M'),
#                 topics = topics_selected,
#                 multiple_retries=False,
#                 active=False
#                 )
#     create_quiz_all_users('FA23-Monday',quiz_id)
#     create_quiz_all_users('FA23-Thursday',quiz_id)
