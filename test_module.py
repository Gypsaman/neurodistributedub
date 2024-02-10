from webproject import create_app, db
from webproject.models import User, Submissions, Attendance
from graders.check_submissions import check_submissions

with create_app().app_context():
    for attend in Attendance.query.all():
        print(attend)




        

    
    

    




