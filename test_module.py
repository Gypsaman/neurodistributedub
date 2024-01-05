from webproject import create_app,db
from webproject.models import Quiz_Header,Assignments
from webproject.modules.create_initial_data import create_users_from_roster,create_initial_data
with create_app().app_context():
    create_initial_data()
exit()

with create_app().app_context():
    print('Quizzes')
    for qh in Quiz_Header.query.all():
        print(qh.id,qh.description)
    print('Assignments')
    for assgn in Assignments.query.all():
        print(assgn.id,assgn.name)



