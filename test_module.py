from graders.check_submissions import check_submissions
from webproject.modules.table_creator import TableCreator,Field, only_contract, timestamp_to_date
from webproject import db, create_app
from webproject.modules.ubemail import UBEmail
from webproject.models import Submissions, User,Grades
from webproject.modules import offline_utils as ou
from webproject.modules import roster
import pandas as pd
import json

# with open('test.json') as f:
#     data = json.load(f)
# print(set([d['assignment'] for  d in data]))

# # df = ou.grade_history_data()
# # print(df.head())



# check_submissions()

try:
    var1
except NameError:
    var1 = 1
    
print(var1)