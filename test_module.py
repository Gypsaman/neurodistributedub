from graders.check_submissions import check_submissions
<<<<<<< HEAD
import os

print(os.getenv("DATABASE"))
print(os.getenv("SECRET_KEY"))
print(os.getenv("EMAIL_SERVER"))

# check_submissions()
=======
from webproject import create_app, db
from webproject.models import Submissions
# with create_app().app_context():
#     sub = Submissions.query.filter_by(user_id=1,assignment=12).first()
#     sub.grade = None
#     db.session.commit()
    
check_submissions()
>>>>>>> fd98ee3b83d6ff335d5d95f12c95aba692b2fd54
