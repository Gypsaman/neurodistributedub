from webproject.modules.offline_utils import grade_update
from webproject.modules.quizzes import create_quiz_all_users
from webproject import db, create_app
from webproject.models import Quizzes, User
from graders.check_submissions import check_submissions

check_submissions()
# with create_app().app_context():

#     quizzes = Quizzes.query.filter_by(id=112).first()
#     db.session.delete(quizzes)
#     db.session.commit()
topic = {'Brownie':15}
create_quiz_all_users('SP23-Wednesday','Brownie',topic)

