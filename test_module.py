from graders.check_submissions import check_submissions
from webproject import create_app, db
from webproject.models import Submissions
# with create_app().app_context():
#     sub = Submissions.query.filter_by(user_id=1,assignment=12).first()
#     sub.grade = None
#     db.session.commit()
    
check_submissions()
