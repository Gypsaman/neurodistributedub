from graders.check_submissions import check_submissions
from webproject.modules.table_creator import TableCreator,Field, only_contract, timestamp_to_date
from webproject import db, create_app
from webproject.modules.ubemail import UBEmail
from webproject.models import Submissions, User
from webproject.modules import offline_utils, roster
from datetime import datetime as dt

offline_utils.import_quiz('Mid Term Quiz',dt.strptime('02/13/2023 20:30', "%m/%d/%Y %H:%M"))

# offline_utils.grade_update('SP23-Monday')
# check_submissions()
# with create_app().app_context():
#     user = User.query.filter_by(student_id='1164271').first()
#     submissions = Submissions.query.filter_by(id=778).all()
#     for sub in submissions:
#         sub.grade = None
#     db.session.commit()
    