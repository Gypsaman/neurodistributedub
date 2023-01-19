from webproject.models import User, Wallet, Assets, Transactions, Assignments,Submissions, Grades, Sections, DueDates
from webproject import create_app, db

from datetime import datetime as dt

def print_data():
    with create_app().app_context():
        
        print('list of users...')
        users = User.query.all()
        if len(users) == 0:
            print("\tNo users found")
        for user in users:
            print(f'\t{user}')
            
        return
        
        print('list of wallets...')
        wallets = Wallet.query.all()
        if len(wallets) == 0:
            print("\tNo wallets found")
        for wallet in wallets:
            print(f'\t{wallet}')
            
        print('list of transactions...')
        transactions = Transactions.query.all()
        if len(transactions) == 0:
            print("\tNo transactions found")
        for transaction in transactions:
            print(f'\t{transaction}')
            
        print('list of assets...')
        assets = Assets.query.all()
        if len(assets) == 0:
            print("\tNo assets found")
        for asset in assets:
            print(f'\t{asset}')
            
        print('list of assignments...')
        assignments = Assignments.query.all()
        if len(assignments) == 0:
            print("\tNo assignments found")
        for assignment in assignments:
            print(f'\t{assignment}')
            
        print('list of submissions...')
        submissions = Submissions.query.all()
        if len(submissions) == 0:
            print("\tNo submissions found")
        for submission in submissions:
            print(f'\t{submission}')
            
        print('list of grades...')
        grades = Grades.query.all()
        if len(grades) == 0:
            print("\tNo grades found")
        for grade in grades:
            print(f'\t{grade}')
            
        print('List of sections')
        sections = Sections.query.all()
        if len(sections) == 0:
            print("\tNo sections found")
        for section in sections:
            print(f'\t{section}')
            
        print('List of due dates')
        duedates = DueDates.query.all()
        if len(duedates) == 0:
            print("\tNo due dates found")
        for duedate in duedates:
            print(f'\t{duedate}')
            

           
def delete_rows(table):
    with create_app().app_context():
        rows = table.query.all()
        for row in rows:
            db.session.delete(row)
            db.session.commit()
            
def get_column(table,column):
    with create_app().app_context():
        rows = table.query.all()
        col = []
        for row in rows:
            col.append(getattr(row,column))
            break
        return col

def add_sections():
    with create_app().app_context():
        section = Sections(section='SP23-Monday',active=True)
        db.session.add(section)
        section = Sections(section='SP23-Wednesday',active=True)
        db.session.add(section)

        db.session.commit()
        
def update_student_section():
    import json
    with open('./data/roster.json','r') as f:
        roster = json.load(f)
        
    with create_app().app_context():
        
        students = User.query.filter_by(role='student').all()
        for student in students:
            section = Sections.query.filter_by(section=roster[student.student_id]['Course']).first()
            student.section = section.id
            db.session.commit()

if __name__ == '__main__':

    print_data()
