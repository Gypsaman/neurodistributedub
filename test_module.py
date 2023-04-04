from webproject.modules.offline_utils import grade_update
from webproject.modules.quizzes import create_quiz_all_users, Topics, create_quiz
from webproject import db, create_app
from webproject.models import Quizzes, User
from graders.check_submissions import check_submissions
from datetime import datetime,timedelta

print(Topics)
topics = {"NFT":11}
with create_app().app_context():
    create_quiz_all_users('SP23-Monday','NFT',topics)

