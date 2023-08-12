from webproject import models
from webproject import create_app, db
from webproject.models import User, Sections
from werkzeug.security import generate_password_hash

def create_initial_data():

    with create_app().app_context():
        
        create_sections()
        create_user()
        
        
def create_quizzes():
    pass

def create_sections():
    section = Sections(
        section='FA23-Monday',
        active = True
    )
    db.session.add(section)
    db.session.commit()
def create_user():
    section = Sections.query.filter_by(section='FA23-Monday').first() 
    user = User(
        email='gypsaman@gmail.com',
        password=generate_password_hash('123',method='sha256'),
        first_name='Cesar',
        last_name ='Garcia',
        student_id='553029',
        role='admin',
        section=section.id
        )
    db.session.add(user)
    db.session.commit()
        
if __name__ == '__main__':
    create_initial_data()