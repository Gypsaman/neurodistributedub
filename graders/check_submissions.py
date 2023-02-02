from webproject import create_app, db
from webproject.models import Assignments,Submissions,Grades, User, DueDates
from webproject.modules.ubemail import UBEmail
from datetime import datetime as dt
from graders.grader import call_grader
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
            
                try :
                    assignment = Assignments.query.filter_by(id=submission.assignment).first()
                    
                    submission_content = os.path.join(UPLOAD_FOLDER,submission.submission) if assignment.inputtype == 'file' else submission.submission
                    
                    if assignment.grader == 'None':
                        grade=0
                        comments='No grader assigned'
                    else:
                        grade,comments = call_grader(assignment.name,submission_content)
                    
                    grade,comments = update_if_late(submission.date_submitted,assignment.id,submission.user_id,grade,comments)
                    
                    update_grade(submission,grade,comments)

                    email_grade(submission,assignment,grade,comments)
                    
                    if assignment.inputtype == 'file':
                        shutil.move(submission_content,os.path.join(STORE_FOLDER,submission.submission))
                
                except Exception as e:
                    email_error(e)
                    exit()
            
            time.sleep(30)
            

def update_if_late(date_submitted,assignment_id,user_id,grade,comments):
    user = User.query.filter_by(id=user_id).first()
    due_date = DueDates.query.filter_by(assignment=assignment_id,section=user.section).first()
    if date_submitted > due_date.duedate:
        days = (date_submitted - due_date.duedate).days
        grade = grade - 5 if days < 7 else grade - 11
        comments += f'\n\nyour submission was {days} days late'
    return grade,comments

def email_grade(submission,assignment,grade,comments):
    email = UBEmail()
    user = User.query.filter_by(id=submission.user_id).first()
    body = f'Your grade for {assignment.name} is {grade}\n\nComments on grade:\n{comments}'
    email.send_email(user.email,f'Grade for {assignment.name}',body)
    
def email_error(error):
    email = UBEmail()
    body = f'Check_submissions error:\n{error}'
    email.send_email('cegarcia@bridgeport.edu',f'Check_submissions error',body)
    
def update_grade(submission,grade,comments):
    submission.grade = grade
    submission.comment = comments
    grade = Grades.query.filter_by(assignment=submission.assignment,user_id=submission.user_id).first()
    if grade is None:
        grade = Grades(user_id=submission.user_id,assignment=submission.assignment,grade=submission.grade,dategraded=dt.now())
        db.session.add(grade)
    else:
        grade.grade = max(submission.grade,grade.grade)
        grade.dategraded = dt.now()
    db.session.commit()
                


if __name__ == '__main__':
    check_submissions()