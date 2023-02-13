from graders.check_submissions import check_submissions
from webproject.modules.table_creator import TableCreator,Field, only_contract, timestamp_to_date
from webproject import db, create_app
from webproject.modules.ubemail import UBEmail

check_submissions()
# import json
# from webproject.modules import roster

# data = roster.open_roster_encrypted()
# with open('./data/practicequiz.csv','r') as f:
#     quiz = f.readlines()

# canvas = {data[l]['Canvas ID']:data[l]['Preferred Email'] for l in data}

# for line in quiz[1:]:
#     email = UBEmail()
#     body = f'You have not worked on your practice quiz.  This will be very important for the midterms on Wendesday.  Please work on it as soon as possible.\nThanks,\nCesar'
#     email.send_email(canvas[line.replace('\n','')],'Practice Quiz',body)

# from webproject.modules import offline_utils

# # offline_utils.grade_history()
# offline_utils.Assignments_not_completed()
