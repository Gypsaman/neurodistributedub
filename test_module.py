from webproject import create_app, db
from webproject.models import User, Submissions, Attendance
from graders.check_submissions import check_submissions
from graders.MidTermExam import build_exam_distribution,email_exams

with create_app().app_context():
    build_exam_distribution()
    email_exams(section=1)




        

    
    

    




