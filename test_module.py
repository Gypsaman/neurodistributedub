from graders.check_submissions import check_submissions
from webproject.modules.table_creator import TableCreator,Field, only_contract, timestamp_to_date
from webproject import db, create_app
from webproject.modules.ubemail import UBEmail
from webproject.models import Submissions, User,Grades



# offline_utils.import_quiz('Practice Quiz',dt.strptime('02/14/2023 16:30', "%m/%d/%Y %H:%M"))

# offline_utils.grade_update('SP23-Monday')
# with create_app().app_context():
#     user = User.query.filter_by(student_id='1161704').first()
#     submissions = Submissions.query.filter_by(id=912).all()
#     for subm in submissions:
#         subm.grade = None
#     db.session.commit()
    
        
check_submissions()
# with open('test.json','r') as f:
#     students = f.readlines()
# students = [student.strip().replace('/n','') for student in students]

# with create_app().app_context():
#     grades = Grades.query.filter_by(assignment=6).all()
#     found = 1
#     for grade in grades:
#         user=User.query.filter_by(id=grade.user_id).first()
#         if user.section == 1:
#             continue
#         if user.student_id not in students:
#             print(user.student_id,user.email)
#         else:
#             found += 1
#     print(found)
            
    
        
# check_submissions()