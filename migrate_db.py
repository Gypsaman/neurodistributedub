from webproject import models
from webproject import create_app, db

with create_app().app_context():
    db.migrate()
    db.upgrade()