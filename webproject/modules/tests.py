from webproject import create_app, db
from webproject.models import User
from werkzeug.security import generate_password_hash, check_password_hash

def create_test_users():
    with create_app().app_context():
        user = User(first_name='Test',last_name='User',email='fake1@gmail.com',role='student',section=1,password=generate_password_hash('123456',method='sha256'))
        db.session.add(user)
        user = User(first_name='Test',last_name='User2',email='fake2@gmail.com',role='student',section=1,password=generate_password_hash('123456',method='sha256'))
        db.session.add(user)
        db.session.commit()
        
        