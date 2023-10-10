from flask_login import UserMixin
from webproject.modules.extensions import db
from datetime import datetime


class Sections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(10), unique=True)
    active = db.Column(db.Boolean)
    
    def __repr__(self):
        return f'section: {self.section}, active: {self.active}'

class User(UserMixin,db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    student_id = db.Column(db.String(10),unique=True)
    section = db.Column(db.Integer, db.ForeignKey('sections.id'))
    role = db.Column(db.String(10))
    
    def get_urole(self):
        return self.role
    
    def __repr__(self):
        return f'email: {self.email}, first_name: {self.first_name}, last_name: {self.last_name}, student_id: {self.student_id}, section: {self.section}, role: {self.role} '

class PasswordReset(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    password_phrase = db.Column(db.Integer)
    phrase_expires = db.Column(db.DateTime)
    
    def get_password_phrase(self):
        return self.password_phrase
    
    def get_password_phrase_expiry(self) -> datetime:
        return self.phrase_expires
    
    def __repr__(self):
        return f'password_phrase: {self.password_phrase}, phrase_expires: {self.phrase_expires}'

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    wallet = db.Column(db.Integer)
    privatekey = db.Column(db.Integer)
    
    def __repr__(self):
        return f'student_id: {self.user_id}, wallet: {self.wallet}, privatekey: {self.privatekey}'
    
class Assets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    asset_type = db.Column(db.Integer)
    network = db.Column(db.String(10))
    asset_address = db.Column(db.Integer,unique=True)
    time_added = db.Column(db.DateTime)
    assignment = db.Column(db.Integer)
    
    def __repr__(self):
        return f'student_id: {self.user_id}, asset_type: {self.asset_type}, network: {self.network}, asset_address: {self.asset_address}, time_added: {self.time_added}, assignment: {self.assignment}'
    
class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
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
    # instructions = db.Column(db.String(100))
    inputtype = db.Column(db.String(10))
    grader = db.Column(db.String(50))
    active = db.Column(db.Boolean)
    
    
    def __repr__(self):
        return f'name: {self.name}, inputtype: {self.inputtype}, grader: {self.grader}, active: {self.active}'
    
class DueDates(db.Model):
    __tablename__ = 'due_dates'
    id = db.Column(db.Integer, primary_key=True)
    assignment = db.Column(db.Integer, db.ForeignKey('assignments.id'))
    section = db.Column(db.Integer,db.ForeignKey('sections.id'))
    duedate = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'assignment: {self.assignment}, section: {self.section}, duedate: {self.duedate}'
    

class Grades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    assignment = db.Column(db.Integer, db.ForeignKey('assignments.id'))
    grade = db.Column(db.Integer)
    dategraded = db.Column(db.DateTime)
    
    assignmentR = db.relationship('Assignments', backref='grades', lazy=True)
   
    def __repr__(self):
        return f'assignment: {self.assignment}, grade: {self.grade}, dategraded: {self.dategraded}'
    
    
class Submissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    assignment = db.Column(db.Integer, db.ForeignKey('assignments.id'))
    submission = db.Column(db.String(100))
    date_submitted = db.Column(db.DateTime)
    grade = db.Column(db.Integer)
    comment = db.Column(db.String(100))
    
    
    def __repr__(self):
        return f'user_id: {self.user_id}, assignment: {self.assignment}, submission: {self.submission}, date_submitted: {self.date_submitted}, grade: {self.grade}, comment: {self.comment}'   
    
class Quiz_Header(db.Model):
    __tablename__ = 'quiz_header'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    date_available = db.Column(db.DateTime)
    date_due = db.Column(db.DateTime)
    multiple_retries = db.Column(db.Boolean)
    active = db.Column(db.Boolean)
    
    def __repr__(self):
        return f'id: {self.id} description: {self.description} date available: {self.date_available} date due {self.date_due} multiple retires {self.multiple_retries} active {self.active}'
    
class Quiz_Topics(db.Model):
    __tablename__ = 'quiz_topics'
    id = db.Column(db.Integer, primary_key=True)
    quiz_header = db.Column(db.Integer, db.ForeignKey('quiz_header.id'))
    topic = db.Column(db.String(100))
    number_of_questions = db.Column(db.Integer)
    
    def __repr__(self):
        return f'topic {self.topic} number of questions {self.number_of_questions}'
    
class Quizzes(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    quiz_header = db.Column(db.Integer, db.ForeignKey('quiz_header.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    submitted = db.Column(db.Boolean)
    grade = db.Column(db.Integer)
    
    def __repr__(self):
        return f'quiz_header: {self.quiz_header}, user_id: {self.user_id}, submitted: {self.submitted}, grade: {self.grade}'
    
class Questions(db.Model):
    __tablename__ = 'questions'
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'),primary_key=True)
    question_id = db.Column(db.String(10),primary_key=True)
    topic = db.Column(db.String(50))
    question = db.Column(db.String(500))
    display_order = db.Column(db.Integer)
    answer_chosen = db.Column(db.String(20))
    is_correct = db.Column(db.Boolean)
    
    def __repr__(self):
        return f'id: {self.question_id} topic: {self.topic}  question: {self.question} display order: {self.display_order} answer chosen: {self.answer_chosen} correct: {self.is_correct}'
    
class Answers(db.Model):
    __tablename__ = 'answers'
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'),primary_key=True)
    question_id = db.Column(db.String(10),db.ForeignKey('questions.question_id'), primary_key=True )
    answer_id = db.Column(db.String(10),primary_key=True)
    display_order = db.Column(db.Integer)
    answer_txt = db.Column(db.String(100))
    correct_answer = db.Column(db.Boolean)
    
    def __repr__(self):
        return f'id: {self.answer_id}, Display Order: {self.display_order}, Text: {self.answer_txt}, Correct Answer? :{self.correct_answer}'
    

    
    