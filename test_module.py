from webproject import create_app, db
from webproject.models import User, Submissions, Attendance
from graders.check_submissions import check_submissions
from graders.MidTermExam import build_exam_distribution,email_exams
from webproject.modules.create_initial_data import check_user_to_roster,create_users_from_roster

with create_app().app_context():
    # build_exam_distribution()
    
    # email_exams(section=1)
    
    for user in User.query.filter_by(email='pgondhi@my.bridgeport.edu').all():
        user.role='student'
        user.section = 2
        db.session.commit()
    check_user_to_roster()
    create_users_from_roster()
    print(User.query.filter_by(role='student',section=1).count())
    print(User.query.filter_by(role='student',section=2).count())




        

    
    

    




