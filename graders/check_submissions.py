from webproject import create_app, db
from webproject.models import Assignments,Submissions,Grades
from webproject.modules.ubemail import UBEmail
import time
from datetime import datetime as dt
from graders.grader import call_grader
import os
from dotenv import load_dotenv

def check_submissions():
    cwd = os.getcwd()
    cwd = os.path.join(cwd, 'neurodistributedub') if cwd == '/home/neurodistributed' else cwd
    
    load_dotenv(os.path.join(cwd, '.env'))
    UPLOAD_FOLDER = os.getenv('UPLOADPATH')

    with create_app().app_context():
        submissions = Submissions.query.filter_by(grade=None).all()
        for submission in submissions:
            submissionPath = os.path.join(UPLOAD_FOLDER,submission.submission)
            assignment = Assignments.query.filter_by(id=submission.assignment).first()
            grade = call_grader(assignment.name,submissionPath)
            submission.grade = grade
            db.session.commit()
        time.sleep(30)
            
            



if __name__ == '__main__':
    check_submissions()