from flask_login import UserMixin
from . import db

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    student_id = db.Column(db.String(10),unique=True)
    role = db.Column(db.String(10))
    
    def get_urole(self):
        return self.role
    
    def __repr__(self):
        return f'email: {self.email}, first_name: {self.first_name}, last_name: {self.last_name}, student_id: {self.student_id}, role: {self.role}'
    
class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(10))
    wallet = db.Column(db.Integer)
    privatekey = db.Column(db.Integer)
    
    def __repr__(self):
        return f'student_id: {self.student_id}, wallet: {self.wallet}, privatekey: {self.privatekey}'
    
class Assets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(10))
    asset_type = db.Column(db.Integer)
    network = db.Column(db.String(10))
    asset_address = db.Column(db.Integer,unique=True)
    time_added = db.Column(db.DateTime)
    assignment = db.Column(db.Integer)
    
    def __repr__(self):
        return f'student_id: {self.student_id}, asset_type: {self.asset_type}, network: {self.network}, asset_address: {self.asset_address}, time_added: {self.time_added}, assignment: {self.assignment}'
    
class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallet = db.Column(db.Integer)
    blockNumber = db.Column(db.Integer)
    timeStamp = db.Column(db.DateTime)
    hash = db.Column(db.Integer)
    nonce = db.Column(db.Integer)
    blockHash = db.Column(db.Integer)
    transactionIndex = db.Column(db.Integer)
    trans_from = db.Column(db.Integer)
    trans_to = db.Column(db.Integer)
    value = db.Column(db.Integer)
    gas =  db.Column(db.Integer)
    gasPrice = db.Column(db.Integer)
    isError = db.Column(db.Boolean)
    txreceipt_status = db.Column(db.Boolean)
    input = db.Column(db.String)
    contractAddress = db.Column(db.Integer)
    cumulativeGasUsed = db.Column(db.Integer)
    gasUsed = db.Column(db.Integer)
    confirmations = db.Column(db.String)
    methodId = db.Column(db.String)
    functionName = db.Column(db.String)
    
    
    def __repr__(self):
        return f'wallet: {self.wallet}, blockNumber: {self.blockNumber}, timeStamp: {self.timeStamp}, hash: {self.hash}, from: {self.trans_from}, to: {self.trans_to}'
    
class Assignments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    due = db.Column(db.DateTime)
    inputtype = db.Column(db.String(10))
    grader = db.Column(db.String(50))
    
    def __repr__(self):
        return f'name: {self.name}, due: {self.due}, inputtype: {self.inputtype}, grader: {self.grader}'
    
class Grades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment = db.Column(db.Integer)
    grade = db.Column(db.Integer)
    dategraded = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'assignment: {self.assignment}, grade: {self.grade}, dategraded: {self.dategraded}'
    
    
    