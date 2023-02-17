from graders.check_submissions import check_submissions
from webproject.modules.table_creator import TableCreator,Field, only_contract, timestamp_to_date
from webproject import db, create_app
from webproject.modules.ubemail import UBEmail
from webproject.models import Submissions, User,Grades
from webproject.modules import offline_utils as ou
import pandas as pd

df = ou.grade_history_data('SP23-Monday')
table = TableCreator('Grade History',fields={},actions=[],domain='/admin/grade-history/SP23-Monday')
table.dataframe(df,index=['Student ID'])
table.set_items_per_page(15)
html = table.create(1)
print(html)

# check_submissions()