from graders.check_submissions import check_submissions
from webproject.modules.table_creator import TableCreator,Field, only_contract, timestamp_to_date
from webproject import db, create_app
from webproject.modules.ubemail import UBEmail
from webproject.models import Submissions, User,Grades
from webproject.modules import offline_utils as ou


# offline_utils.import_quiz('Practice Quiz',dt.strptime('02/14/2023 16:30', "%m/%d/%Y %H:%M"))

# offline_utils.grade_update('SP23-Monday')
# with create_app().app_context():
#     user = User.query.filter_by(student_id='1166070').first()
#     submissions = Submissions.query.filter_by(user_id=user.id,assignment=9,id=1191).all()
#     for subm in submissions:
#         # print(subm,subm.id)
#         subm.grade = None
#     db.session.commit()
    
        
check_submissions()
# df = ou.grade_history_data()
# table = TableCreator('Grade History',fields={},actions=[])
# table.dataframe(df,index=['Section','Student ID'])
# table.set_items_per_page(15)
# html = table.create(1)
# print(html)

    
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