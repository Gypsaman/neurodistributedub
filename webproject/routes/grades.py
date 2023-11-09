import json
from webproject import create_app, db
from webproject.models import Assignments, User, Wallet, Quiz_Header
from graders.final_grade import final_grades_student


def get_letter_grade():
    with create_app().app_context():
            
        for assgn in Assignments.query.all():
                assgn.name = assgn.name.strip()
        db.session.commit()
        all_students = {}

        for user in User.query.filter_by(role='student').all():
            print(user)
            final_grades = final_grades_student(user.id)
            final_grades['email']   = user.email
            final_grades['section'] = user.section
            wallet = Wallet.query.filter_by(user_id=user.id).first()
            final_grades['wallet'] = wallet.wallet if wallet else ""
            
                
            all_students[user.student_id] = final_grades
            
        json.dump(all_students,open('summary.json','w'),indent=4)

    all_students = json.load(open('summary.json','r'))    

    columns = []
    for header in Quiz_Header.query.all():
        columns.append(header.description)
    for assignment in Assignments.query.all():
        columns.append(assignment.name)
    # columns = ['Mid Term','Mid Term 2','Midterm Exam','SHA256','ECC Curve','Wallet','PayUB','myID','Encryption','BlockChain','Solidity']


    with open('zero_midterms_details.csv','w') as f:
        
        header = 'section,Student ID,email,wallet'
        for col in columns:
            header += f',{col}'
        f.write(f'{header}\n')
        for student_id,student in all_students.items():
            data =  f"{student['section']},{student_id},{student['email']},{student['wallet']}"
            for col in columns[:3]:
                data += ','
                data += str(student['Midterms'][col]['score']) if col in student['Midterms'] else ''
            for col in columns[3:]:
                data += ','
                data += str(student['Assignments'][col]['score']) if col in student['Assignments'] else ''
            data += '\n'
            f.write(data)
        