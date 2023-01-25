# from webproject.modules.roster import not_registered

# print(not_registered('SP23-Monday',True))

# from graders import check_submissions

# check_submissions.check_submissions()

from webproject import db, create_app
from webproject.models import Assignments,Submissions,Grades, User

with create_app().app_context():
    submissions = Submissions.query.filter_by(grade=None).all()
    for submission in submissions:
        submission.grade = 20
    db.session.commit()