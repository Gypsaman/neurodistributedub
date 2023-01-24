from webproject import db, create_app
from webproject.models import User

with create_app().app_context():
    user = User.query.filter_by(student_id='1148972').first()
    user.eamil = 'sthotla@my.bridgeport.edu'
    db.session.c