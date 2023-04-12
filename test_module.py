from webproject.modules.offline_utils import grade_update
from webproject.modules.quizzes import create_quiz_all_users, Topics, create_quiz, create_final
from webproject import db, create_app
from webproject.models import Quizzes, User
from graders.check_submissions import check_submissions
from datetime import datetime,timedelta


questions = sum([val for key,val in Topics.items()])
perc = 60/questions
total = 0
topic_selected = {}
for key,val in Topics.items():
    qty = round(val*perc)
    topic_selected[key] = qty
    total += qty
if total > 60:
    topic_selected['Brownie'] -= 1
print(topic_selected)
create_final(topic_selected,datetime.strptime('2023-04-14 17:00','%Y-%m-%d %H:%M'))

