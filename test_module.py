from graders.check_submissions import check_submissions
from webproject import create_app, db
from webproject.models import Submissions, Questions
# with create_app().app_context():
#     sub = Submissions.query.filter_by(user_id=1,assignment=12).first()
#     sub.grade = None
#     db.session.commit()

from webproject.modules.quizzes import create_quiz_all_users,Topics, questions, create_quiz

print(Topics)


from datetime import datetime as dt
from time import timedelta
topics = {"Brownie": 15}
description = 'Brownie'
create_quiz(topics,dt.now(),dt.now()+timedelta(days=7),description=description + ' for Cesar',user_id=1)
# create_quiz_all_users('SP23-Monday','Brownie',topics)
