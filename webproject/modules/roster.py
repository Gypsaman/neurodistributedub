from webproject import db, create_app
from webproject.models import User, Submissions, Grades, Sections, Assignments
from webproject.modules.ubemail import UBEmail
import json
import os
from webproject.modules.dotenv_util import initialize_dotenv,get_cwd
import fernet

initialize_dotenv()
filepath = get_cwd()


def convert_roster_csv():
    with open(os.path.join(filepath,'roster.csv','r')) as f:
        roster = f.readlines()
        
    columns = roster[0][:-1].split(',')
    
    out = {}
    if os.path.exists(os.path.join(filepath,'roster.enc')):
        out = open_roster_encrypted()
    
    for line in roster[1:]:
        data = line.split(',')
        student_id = data[0]
        if student_id in out:
            continue
        info = {columns[i]:data[i] for i in range(1,len(columns))}
        info['Course'] = info['Course'][:-1]
        out[student_id] = info
        
    save_roster_encrypted(out)
      
def create_registered_item():
    roster = open_roster_encrypted()
        
    for student in roster:
        roster[student]['Registered'] = False

    save_roster_encrypted(roster)

def update_registered():
    roster = open_roster_encrypted()

    with create_app().app_context():
        users = User.query.all()
        for user in users:
            if user.role == 'student':
                roster[user.student_id]['Registered'] = True
        
    save_roster_encrypted(roster)

def not_registered(section,listonly=False):
    roster = open_roster_encrypted()
    
    not_registered = []
    for student in roster:
        if roster[student]['Course'] == section:
            if roster[student]['Registered'] == False:
                not_registered.append(roster[student]['Preferred Email'])
    
    if listonly:
        return not_registered
    
    body = f'Dear Student,\n\nYou have not registered on the website for homework submission.  Please go to www.neurodistributed.com to register.\n\nCesar'
    for email_address in not_registered:
        email = UBEmail()
        email.send_email(email_address,'Register in Website',body)
    
    return None

def assignment_not_submitted(assignment,listonly=False):
    with create_app().app_context():
        not_submitted = []
        assignment = Assignments.query.filter_by(name=assignment).first()
        users = User.query.filter_by(section=2).all()
        for user in users:
            submission = Submissions.query.filter_by(user_id=user.id,assignment=assignment.id).first()
            if submission == None:
                not_submitted.append(user.email)
    
    if listonly:
        return not_submitted
    
    body = f'Dear Student,\n\nYou have not submitted assignment {assignment}.\n\nAssignment is past due date\n\nCesar'
    for email_address in not_submitted:
        email = UBEmail()
        email.send_email(email_address,'Register in Website',body)
    
    return None

def open_roster_encrypted():
    key = bytes(os.environ.get('FERNET_KEY').encode('utf-8'))
    with open('./data/roster.enc','rb') as f:
        roster = f.read()
    frn = fernet.Fernet(key)
    roster = frn.decrypt(roster).decode('utf-8')
    
    return json.loads(roster)

def save_roster_encrypted(roster):
    key = bytes(os.environ.get('FERNET_KEY').encode('utf-8'))
    frn = fernet.Fernet(key)
    roster = frn.encrypt(roster)
    
    with open('./data/roster.enc','wb') as f:
        f.write(roster)
    
    return None

if __name__ == '__main__':

    roster = open_roster_encrypted()
    print(roster)
    
