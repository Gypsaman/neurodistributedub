from graders.check_submissions import check_submissions
from webproject import create_app, db
from webproject.models import Submissions, Questions
# with create_app().app_context():
#     sub = Submissions.query.filter_by(user_id=1,assignment=12).first()
#     sub.grade = None
#     db.session.commit()

from webproject.modules.quizzes import create_quiz_all_users,Topics, questions

print(Topics)
def update_topics():
    with create_app().app_context():
        db_questions = Questions.query.all()
        for q in db_questions:
            topic = questions[q.question_id]['Topic']
            q.topic = topic
        db.session.commit()
            
update_topics()
    
topics = {"Brownie": 15}
create_quiz_all_users('SP23-Monday','Brownie',topics)
