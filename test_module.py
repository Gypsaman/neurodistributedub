from webproject import db, create_app
from webproject.models import User, Wallet
from werkzeug.security import generate_password_hash


def create_user():
    with create_app().app_context():
        user = User(first_name='John', last_name='Doe',student_id='99999',section=1,email='cegarcia@bridgeport.edu', password=generate_password_hash('123456', method='sha256'),role='student')
        db.session.add(user)
        db.session.commit()
    
def list_users():
    with create_app().app_context():
        users = User.query.all()
        for user in users:
            print(user.id, user.email, user.student_id)

def remove_wallet():
    with create_app().app_context():
        user = User.query.filter_by(email='cegarcia@bridgeport.edu').first()
        wallet = Wallet.query.filter_by(user_id=user.id).first()
        db.session.delete(wallet)
        db.session.commit()
            
remove_wallet()