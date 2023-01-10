from webproject import create_app, db
from webproject.models import Assignments,Submissions,Grades, User,Assets
from webproject.modules.table_creator import TableCreator, Field,timestamp_to_date,short_hash,wei_to_eth,asset_type_string,yes_no


with create_app().app_context():
    
    # qry = db.session.execute("Select assignments.name, grade from Grades join Assignments on Grades.assignment = Assignments.id ")
#     qry = db.session.execute('Select t2.name,t1.grade from Grades as t1 join Assignments as t2 on t1.assignment = t2.id ')
    # 'Select assignment.name,grade,dategraded from Grades join Assignments on Grades.assignment = Assignments.id '
#     for row in qry:
#         print(row)
        
    
    fields = {
        'id': Field(None,None),
        'first_name': Field(None,'First Name'),
        'last_name': Field(None,'Last Name'),
        'email': Field(None,'Email'),
        'student_id': Field(None,'Student ID'),
        'role': Field(None,'Role'),

    }
    
    table_creator = TableCreator('User',fields,actions=['Edit','Delete'])
    table_creator.set_items_per_page(30)
    table_creator.create_view()
    table = table_creator.create(page_num)