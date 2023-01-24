from webproject import db, create_app
from webproject.models import User, Submissions, Grades, Sections, Assignments
from webproject.modules.ubemail import UBEmail
import json

def create_registered_item():
    with open('./data/roster.json','r') as f:
        roster = json.load(f)
        
    for student in roster:
        roster[student]['Registered'] = False

    with open('./data/roster.json','w') as f:
        json.dump(roster,f,indent=4)

def update_registered():
    with open('./data/roster.json','r') as f:
        roster = json.load(f)

    with create_app().app_context():
        users = User.query.all()
        for user in users:
            if user.role == 'student':
                roster[user.student_id]['Registered'] = True
        
    with open('./data/roster.json','w') as f:
        json.dump(roster,f,indent=4)

def not_registered(section,listonly=False):
    with open('./data/roster.json','r') as f:
        roster = json.load(f)
    
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

if __name__ == '__main__':
    # create_registered_item()
    update_registered()

    print(not_registered('SP23-Monday',True))
    # print(assignment_not_submitted('SHA256'))