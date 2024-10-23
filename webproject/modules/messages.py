from webproject import db, create_app
from webproject.modules.ubemail import UBEmail
from webproject.models import User

def email_grades():
    with open('grade_details.csv','r') as f:
        grades = f.readlines()
    columns = grades[0].strip('\n').split(',')
    with create_app().app_context():
        for grade in grades[1:]:
            user = User.query.filter_by(student_id=grade.split(',')[0]).first()
            body = ''
            for idx,score in enumerate(grade.strip('\n').split(',')[3:]):
                body += f'{columns[idx+3]}: {score}\n'
                
            email = UBEmail()
            body = f'{user.first_name},\n\n{body}'
            email.send_email(user.email,f'Grades So Far',body)