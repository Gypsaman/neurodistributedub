import pandas as pd
import json
import requests
from webproject.modules.ubemail import UBEmail
from webproject.modules import roster
from webproject import db, create_app
from webproject.models import User, Assignments, Submissions, Grades, Sections, DueDates, Quizzes, QuestionBank,AnswerBank
from datetime import datetime as dt
from webproject.modules import dotenv_util
import os

extra_credit = ['1195047']

Assignment_qry = "SELECT * from Assignments inner join (SELECT assignment,duedate FROM due_dates WHERE section = {} and duedate <= '{}') as d on Assignments.id = d.assignment"

def import_quiz_questions():
    quizzes = json.load(open('./data/quizzes.json','r'))

    with create_app().app_context():

        for question_number,question in quizzes.items():
                
            topic = question['Topic']
            question_txt = question['Question']
            question_bank = QuestionBank(topic=topic,question=question_txt)
            db.session.add(question_bank)
            db.session.commit()
            db.session.refresh(question_bank)
            for answer in question['Answers']:
                answer_txt = answer['Answer']
                correct_answer = answer['Correct']
                db.session.add(
                    AnswerBank(
                        question_id=question_bank.question_id,
                        answer_txt=answer_txt,
                        correct_answer=correct_answer)
                    )
            db.session.commit()
        print('Done')

def provide_grade_update(section_name=None):
    with create_app().app_context():
        if section_name is None:
            users = User.query.filter_by(role='student').all()
        else:
            section = Sections.query.filter_by(section=section_name).first()
            users = User.query.filter_by(section=section.id,role='student').all()
        assignments = db.session.execute(Assignment_qry.format(section.id,dt.now().strftime("%Y-%m-%d"))).all()
        
        
        for user in users:
            unsbumitted = False
            quizzes = Quizzes.query.filter_by(user_id=user.id).filter(Quizzes.date_due<=dt.now()).all()
            body = f'Hello {user.first_name} {user.last_name},\n\nFor assignments due before: {dt.now().strftime("%Y-%m-%d")} your grades are:\n\n'
            body += f'Assignments:\n\n'
            for assignment in assignments:
                grade = Grades.query.filter_by(user_id=user.id,assignment=assignment.id).first()
                body += f'\t{assignment.name} - {grade.grade}\n' if grade is not None else f'\t{assignment.name} - Not submitted\n'
                if grade is None:
                    unsbumitted = True
            body += f'\nQuizzes:\n\n'
            for quiz in quizzes:
                body += f'\t{quiz.description} - {quiz.grade}\n' 
                if quiz.grade is None or quiz.grade == 0:
                    unsbumitted = True
            if unsbumitted:
                body += '\n\nYou have unsubmitted Assignment(s).  Let me know if you need any help.\n\n'
            email = UBEmail()
            email.send_email(user.email,'Revised Grade Update',body)
            

def grade_history_data(section_name=None):
        
    response = requests.get('http://neurodistributed.com/gradehistory')
    # response = requests.get('http://127.0.0.1:5000/gradehistory')
    gradehistory = json.loads(response.text)
    

    df = pd.json_normalize(gradehistory)
    
    if section_name:
        pt = df[df['section']==section_name].pivot_table(index=['StudentID'], columns='assignment', values='grade', aggfunc='sum')
    else:
        pt = df.pivot_table(index=['section','StudentID'], columns='assignment', values='grade', aggfunc='sum')
            
    return pt
    
def Assignments_not_completed():
    
    students = roster.open_roster_encrypted()
    
    grades = grade_history_data()
    
    columns = grades.columns.tolist()
    for idx,row in grades.iterrows():
        
        body = ''
        for col in columns:
            if pd.isna(row[col]) or row[col] == 0:
                body += f'\t{col}\n'
        if body == '':
            continue
            
        student_id = idx[1]
        
        body = f"{students[student_id]['Student Name']},\n\nYou have not completed the following assignments:\n" + body
        
        if 'Wallet' in body:
            body += f"\n***** YOUR WALLET IS NECESSARY FOR MIDTERMS "
            body += f"\n***** YOUR WILL NOT BE ABLE TO SUBMIT WITHOUT THE WALLET\n"
        
        email = UBEmail()
        email.send_email(students[student_id]['Preferred Email'],'Assignments not completed',body)
        
def import_quiz(quiz_name,quizdate):
    cwd = dotenv_util.get_cwd()
    with create_app().app_context():
        assignment = Assignments.query.filter_by(name=quiz_name).first()
        if assignment is None:
            print(f'Could not find assignment {quiz_name}')
            return
        lookup = {info['Canvas ID']:student for student,info in roster.open_roster_encrypted().items()}
        grades = open(os.path.join(cwd,'data','quizimport.csv'),'r').readlines()
        for grade in grades[1:]:
            student_id,grade = grade.split(',')
            student_id = student_id.strip()
            grade = grade.strip().replace('/n','')
            if student_id not in lookup:
                print(f'Could not find student {student_id}')
                continue
            student = lookup[student_id]
            user = User.query.filter_by(student_id=student).first()
            if user is None:
                print(f'Could not find user {student}')
                continue
            if Grades.query.filter_by(user_id=user.id,assignment=assignment.id).first() is not None:
                print(f'Grade already exists for {student}')
                continue
            grade = Grades(user_id=user.id,assignment=assignment.id,grade=grade,dategraded=quizdate)
            db.session.add(grade)
            db.session.commit() 
    
def email_course_evaluation():
    with create_app().app_context():
        for user in User.query.filter_by(role='student').all():
            email = UBEmail()
            body = f'''Hello {user.first_name} {user.last_name},\n\n'''
            body += f'''Please complete the course evaluation for this course.  It is very important for me to get your feedback.  '''
            body += '\n\nCesar Garcia\n'
            email.send_email(user.email,'Course Evaluation',body)

    
if __name__ == '__main__':
    email_course_evaluation()