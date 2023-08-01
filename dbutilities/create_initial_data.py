from webproject import models
from webproject import create_app, db
from webproject.models import User, Sections
from werkzeug.security import generate_password_hash

def create_initial_data():

    with create_app().app_context():
        section = Sections(
            section='Fall 2023',
            active = True
        )
        db.session.add(section)
        db.session.commit()
        section = Sections.query.filter_by(section='Fall 2023').first() 
        user = User(
            email='gypsaman@gmail.com',
            password=generate_password_hash('b123',method='sha256'),
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