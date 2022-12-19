from webproject import db, create_app, models

with create_app().app_context():
    print('creating db....')
    db.create_all()