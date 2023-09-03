from webproject import models
from webproject import create_app, db
from webproject.models import User, Sections
from werkzeug.security import generate_password_hash
from webproject.modules.quizzes import create_quiz, Topics

import os
import pandas as pd
import hashlib
from webproject.modules.ubemail import UBEmail


def create_initial_data():

    with create_app().app_context():
        db.create_all()
        create_sections()
        create_users()
        


def create_sections():
    sections = ['FA23-Monday','FA23-Thursday']
    for section in sections:
        if Sections.query.filter_by(section=section).first():
            continue
        new_section = Sections(
            section=section,
            active = True
        )
        db.session.add(new_section)
    db.session.commit()
    
def send_new_user_email(first_name,email_addr,pwd):
    body = f'Dear {first_name},\n\n'
    body += 'Welcome to CPSC-570, Blockchain & Crypto Currency Technology.\n'
    body += 'In this course we will be utilizing a web interface for assignments and quizzes.\n\n'
    body += '    Please follow the link: www.neurodistributed.com.\n\n'
    body += f'Your user name is your email address and your password is "{pwd}".  You may change your password at any time.\n\n'
    body += 'I have populated your first name and last name, you may change these as needed.\n\n'
    body += 'If you have any questions, feel free to contact me.\n\n'
    body += 'Cesar Garcia'
    
    email = UBEmail()
    email.send_email(email_addr,'Assignment and Quiz Web Site',body)
    
def create_users_from_roster(top=None):
    roster_dir = './data/rosters'
    email_body = ''
    for roster in os.listdir(roster_dir):
        r_df = pd.read_csv(os.path.join(roster_dir,roster))
        section_name = roster.split('.')[0]
        roster_section = Sections.query.filter_by(section=section_name).first()
        if not roster_section:
            raise('Roster Filename needs to be a valid section')
        
        for idx, student in r_df.iterrows():
            if top and idx > top:
                break
            pwd = hashlib.sha256(bytes(student['Preferred Email']+'cegarcia@bridgeport.edu','utf-8')).hexdigest()[:8]
            if User.query.filter_by(email=student['Preferred Email']).first():
                continue
            lastname = student['Preferred Email'].split('@')[0][1:]
            names = student['Student Name'].split(' ')
            firstname = names[1] 
            if names[1].lower() in ['sai','sri']:
                firstname += ' ' + names[2]

            user = User(
                email = student['Preferred Email'],
                password=generate_password_hash(pwd,method='sha256'),
                first_name= firstname,
                last_name = lastname,
                student_id = student['Student ID'],
                role = 'student',
                section = roster_section.id
                
            )
            db.session.add(user)
            send_new_user_email(user.first_name,user.email,pwd)

            
    db.session.commit()
    
    
def create_users():
    section = Sections.query.filter_by(section='FA23-Monday').first() 
    if not User.query.filter_by(email='gypsaman@gmail.com').first():
            
        user = User(
            email='gypsaman@gmail.com',
            password=generate_password_hash('123',method='sha256'),
            first_name='Cesar',
            last_name ='Garcia',
            student_id='999999',
            role='admin',
            section=section.id
            )
        db.session.add(user)
    if not User.query.filter_by(email='cegarcia@my.brdigeport.edu'):
        user = User(
            email='cegarcia@my.bridgeport.edu',
            password=generate_password_hash('123',method='sha256'),
            first_name='Cesar',
            last_name ='Garcia',
            student_id='553029',
            role='student',
            section=section.id
            )
        db.session.add(user)
    db.session.commit()
    create_users_from_roster()

        
        
       
if __name__ == '__main__':
    create_initial_data()