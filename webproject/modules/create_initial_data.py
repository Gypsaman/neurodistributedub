from webproject import models
from webproject import create_app, db
from webproject.models import User, Sections, Quiz_Header, Quiz_Topics, AnswerBank, QuestionBank, Assignments
from webproject.modules.ubemail import UBEmail
from webproject.modules.quizzes import create_quiz_users
from webproject.models import Quiz_DueDates,Quizzes,Grades,Submissions,DueDates,Sections,User,PasswordReset,Wallet


from werkzeug.security import generate_password_hash
import os
import pandas as pd
import hashlib
import pandas as pd
from sqlalchemy import text
import json

sections = ['FA24-Monday']
SCHEDULE_FILE = './data/Class Topic Schedule.xlsx'

    
def create_initial_data():

    with create_app().app_context():
        create_sections()
        create_users()
        import_assignments_quizzes()
        set_due_dates()

def import_assignments_quizzes():
    quiz_header = json.load(open('./data/quiz_header.json'))
    quiz_topics = json.load(open('./data/quiz_topics.json'))
    for qh in quiz_header:
        qh_id = qh['id']
        qh = Quiz_Header(**{key:value for key,value in qh.items() if key != 'id'})
        db.session.add(qh)
        db.session.commit()
        db.session.refresh(qh)
        for qt in [t for t in quiz_topics if t['quiz_header'] == qh_id]:
            qt = Quiz_Topics(quiz_header=qh.id,topic=qt['topic'],number_of_questions=qt['number_of_questions'])
            db.session.add(qt)
        db.session.commit()
    for assign in json.load(open('./data/assignments.json')):
        assign = Assignments(**{key:value for key,value in assign.items() if key != 'id'})
        db.session.add(assign)
    db.session.commit()
    answer_bank = json.load(open('./data/answer_bank.json'))
    for question in json.load(open('./data/question_bank.json')):
        question_id = question['question_id']
        question = QuestionBank(**{key:value for key,value in question.items() if key != 'id'})
        db.session.add(question)
        db.session.commit()
        db.session.refresh(question)
        for answer in [a for a in answer_bank if a['question_id'] == question_id]:
            curr_answer = {"question_id":question.question_id,"answer_txt":answer['answer_txt'],"correct_answer":answer['correct_answer']}
            db.session.add(AnswerBank(**curr_answer))
        db.session.commit()

        
def create_sections():
    
    for section in sections:
        if Sections.query.filter_by(section=section).first():
            continue
        new_section = Sections(
            section=section,
            active = True
        )
        db.session.add(new_section)
    db.session.commit()
    
def set_due_dates():
    xls = pd.ExcelFile(SCHEDULE_FILE)
    quizzes = pd.read_excel(xls, 'QuizDates')
    for _,quiz in quizzes.iterrows():
        for idx,section in enumerate(sections):
            section_id = Sections.query.filter_by(section=section).first().id
            quiz_header = Quiz_Header.query.filter_by(description=quiz['Description']).first()
            if not quiz_header:
                raise('Quiz Header not found in set_due_dates')
            if not section:
                raise('Section not found in set_due_dates')
            quiz_date = Quiz_DueDates(quiz_header=quiz_header.id,section=section_id, date_due=quiz[f'Section {idx+1}'])
            db.session.add(quiz_date)
        
    db.session.commit()
    assignments = pd.read_excel(xls, 'Assignment Dates')
    for _,assign in assignments.iterrows():
        for idx,section in enumerate(sections):
            section_id = Sections.query.filter_by(section=section).first().id
            assignment = Assignments.query.filter_by(name=assign['Description']).first()
            if not assignment:
                raise('Assignment not found in set_due_dates')
            if not section:
                raise('Section not found in set_due_dates')
            assign_date = DueDates(assignment=assignment.id,section=section_id, duedate=assign[f'Section {idx+1}'])
            db.session.add(assign_date)
        
    db.session.commit()
    
    
def send_new_user_email(first_name,email_addr,pwd):
    body = f'Dear {first_name},\n\n'
    body += 'Welcome to CPSC-570, Blockchain & Crypto Currency Technology.\n'
    body += 'In this course we will be utilizing a web interface for assignments and quizzes.\n\n'
    body += '    Please follow the link: crypto.neurodna.xyz.\n\n'
    body += f'Your user name is your email address and your password is "{pwd}".  You may change your password at any time.\n\n'
    body += 'I have populated your first name and last name, you may change these as needed.\n\n'
    body += 'If you have any questions, feel free to contact me.\n\n'
    body += 'Cesar Garcia'
    
    email = UBEmail()
    email.send_email(email_addr,'Assignment and Quiz Web Site',body)
    
def create_users_from_roster(top=None):
    roster_dir = './data/rosters'
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
                password=generate_password_hash(pwd,method='pbkdf2sha256'),
                first_name= firstname,
                last_name = lastname,
                student_id = student['Student ID'],
                role = 'student',
                section = roster_section.id
                
            )
            db.session.add(user)
            send_new_user_email(user.first_name,user.email,pwd)

            
    db.session.commit()
def check_user_to_roster():
    roster_dir = './data/rosters'
    for roster in os.listdir(roster_dir):
        r_df = pd.read_csv(os.path.join(roster_dir,roster))
        section_name = roster.split('.')[0]
        roster_section = Sections.query.filter_by(section=section_name).first()
        if not roster_section:
            raise('Roster Filename needs to be a valid section')
        print(roster_section.id)
        for user in User.query.filter_by(section=roster_section.id,role='student').all():
            if not r_df[r_df['Preferred Email'] == user.email].empty:
                continue
            else:
                print(f'User {user.email} not found in roster')
                user.role='inactive'
                db.session.commit()
        
def create_users():
    section = Sections.query.filter_by(section=sections[0]).first() 
    if not User.query.filter_by(email='gypsaman@gmail.com').first():
            
        user = User(
            email='gypsaman@gmail.com',
            password=generate_password_hash('123',method='pbkdf2:sha256'),
            first_name='Cesar',
            last_name ='Garcia',
            student_id='999999',
            role='admin',
            section=section.id
            )
        db.session.add(user)
    if not User.query.filter_by(email='cegarcia@my.bridgeport.edu').first():
        user = User(
            email='cegarcia@my.bridgeport.edu',
            password=generate_password_hash('123',method='pbkdf2:sha256'),
            first_name='Cesar',
            last_name ='Garcia',
            student_id='553029',
            role='student',
            section=section.id
            )
        db.session.add(user)
    db.session.commit()
    create_users_from_roster()

def create_user_quizzes():
    for qh in Quiz_Header.query.all():
        quiz_header = qh.id
        stmt = "SELECT user.id FROM user  left join "
        stmt += f"(select quiz_header,user_id from Quizzes where quiz_header = {quiz_header})"
        stmt += "on user.id = user_id where user_id is null"

        users = list(db.session.execute(text(stmt)))

        create_quiz_users(quiz_header,users)
        
       
if __name__ == '__main__':
    set_due_dates()