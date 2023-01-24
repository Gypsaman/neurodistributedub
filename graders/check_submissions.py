from webproject import create_app, db
from webproject.models import Assignments,Submissions,Grades, User
from webproject.modules.ubemail import UBEmail
from datetime import datetime as dt
from graders.grader import call_grader
from dotenv import load_dotenv
from webproject.modules.dotenv_util import initialize_dotenv
import shutil
import os
import time



def check_submissions():
    
    initialize_dotenv()
    
    UPLOAD_FOLDER = os.getenv('UPLOADPATH')
    STORE_FOLDER = os.getenv('STOREPATH')
    
    if os.getenv('ENV') == 'prod':
        os.environ["TZ"] = "America/New_York"
        time.tzset()

    with create_app().app_context():
        while True:
            submissions = Submissions.query.filter_by(grade=None).all()
            for submission in submissions:
                submissionPath = os.path.join(UPLOAD_FOLDER,submission.submission)
                assignment = Assignments.query.filter_by(id=submission.assignment).first()
                grade,comments = call_grader(assignment.name,submissionPath)
                
                submission.grade = grade
                grade = Grades.query.filter_by(assignment=submission.assignment,user_id=submission.user_id).first()
                if grade is None:
                    grade = Grades(user_id=submission.user_id,assignment=submission.assignment,grade=submission.grade,dategraded=dt.now())
                    db.session.add(grade)
                else:
                    grade.grade = max(submission.grade,grade.grade)
                    grade.dategraded = dt.now()
                db.session.commit()
                
                email = UBEmail()
                user = User.query.filter_by(id=submission.user_id).first()
                body = f'Your grade for {assignment.name} is {grade.grade}\n\nComments on grade:\n{comments}'
                email.send_email(user.email,f'Grade for {assignment.name}',body)
                shutil.move(submissionPath,os.path.join(STORE_FOLDER,submission.submission))
            time.sleep(30)
            
            



if __name__ == '__main__':
    check_submissions()