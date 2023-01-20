from webproject import db, create_app
from webproject.models import User, Submissions, Grades

with create_app().app_context():
    submissions = Submissions.query.all()
    for submission in submissions:
        user = User.query.filter_by(id=submission.user_id).first()
        if user is None:
            print(f'User {submission.user_id} not found for submission {submission.id}')
            continue
        print(user.student_id,submission,user.id)