
from webproject.modules.quizzes import create_quiz, Topics, create_quiz_all_users
from webproject.models import Quizzes, Questions, Answers, Submissions, User, Assignments
from webproject import create_app, db
from datetime import datetime as dt
from graders.check_submissions import check_submissions
import json
from collections import Counter
from webproject.modules.tests import create_test_users

# create_test_users()
topics_selected = {'Web3':15}
create_quiz_all_users('SP23-Monday','Web3 Quiz',topics_selected)

