from webproject import create_app, db
from webproject.models import Assignments,Submissions,Grades, User

with create_app().app_context():
    
    gradeqry = db.session.query(Grades,Assignments).join(Assignments).all()
    
    for grade, assignment in gradeqry:
        print(grade,assignment)
