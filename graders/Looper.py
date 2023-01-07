import time
from webproject import create_app, db
from webproject.models import Submissions
from datetime import datetime as dt
def loop_around():
    with create_app().app_context():
        while True:
            submission = Submissions(user_id=1, 
                                     assignment=1, 
                                     submission='test',
                                     date_submitted = dt.now(),
                                     grade = 100
                                     )
            db.session.add(submission)
            db.session.commit()
            time.sleep(4*60*60)
            
if __name__ == '__main__':
    loop_around()