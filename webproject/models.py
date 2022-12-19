from flask_login import UserMixin
from . import db

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    student_id = db.Column(db.String(10),unique=True)
    
class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(10))
    wallet = db.Column(db.Integer)
    privatekey = db.Column(db.Integer)
    
class Assets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(10))
    asset_type = db.Column(db.Integer)
    network = db.Column(db.String(10))
    asset_address = db.Column(db.Integer,unique=True)