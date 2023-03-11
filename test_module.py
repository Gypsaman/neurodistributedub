from graders.check_submissions import check_submissions
from webproject import create_app, db
from webproject.models import Submissions
# with create_app().app_context():
#     sub = Submissions.query.filter_by(user_id=1,assignment=12).first()
#     sub.grade = None
#     db.session.commit()

from webproject.modules.quizzes import create_quiz_all_users,Topics

print(Topics)
topics = {"Web3": 15}
create_quiz_all_users('SP23-Wednesday','Web3',topics)
