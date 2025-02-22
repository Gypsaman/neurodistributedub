from flask_login import UserMixin
from webproject.modules.extensions import db
from datetime import datetime
import json


def get_dict_from_string(dictstring:str) -> dict:
    try:
        dict = json.loads(dictstring)
    except Exception as e:
        dict = {}
        
    return dict

class Sections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(10), unique=True)
    active = db.Column(db.Boolean)
    


    def __repr__(self):
        return f'section: {self.section}, active: {self.active}'
    
    def to_dict(self):
        return {
            "id": self.id,
            "section": self.section,
            "active": self.active
        }

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
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "student_id": self.student_id,
            "section": self.section,
            "role": self.role
        }

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
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "password_phrase": self.password_phrase,
            "phrase_expires": self.phrase_expires
        }

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    wallet = db.Column(db.Integer)
    privatekey = db.Column(db.Integer)
    
    def __repr__(self):
        return f'student_id: {self.user_id}, wallet: {self.wallet}, privatekey: {self.privatekey}'
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "wallet": self.wallet,
            "privatekey": self.privatekey
        }
    
    
class Assignments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    # instructions = db.Column(db.String(100))
    inputtype = db.Column(db.String(10))
    grader = db.Column(db.String(50))
    active = db.Column(db.Boolean)
    grade_category = db.Column(db.String(50))
    retries = db.Column(db.Integer)
    
    
    def __repr__(self):
        return f'name: {self.name}, inputtype: {self.inputtype}, grader: {self.grader}, active: {self.active}'
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "inputtype": self.inputtype,
            "grader": self.grader,
            "active": self.active,
            "grade_category": self.grade_category,
            "retries": self.retries
        }
    
class DueDates(db.Model):
    __tablename__ = 'due_dates'
    id = db.Column(db.Integer, primary_key=True)
    assignment = db.Column(db.Integer, db.ForeignKey('assignments.id'))
    section = db.Column(db.Integer,db.ForeignKey('sections.id'))
    duedate = db.Column(db.DateTime)
    
    sectioninfo = db.relationship('Sections', lazy='joined')

    def __repr__(self):
        return f'assignment: {self.assignment}, section: {self.section}, duedate: {self.duedate}'
    
    def to_dict(self):
        return {
            "id": self.id,
            "assignment": self.assignment,
            "section": self.section,
            "duedate": self.duedate
        }
    

class Grades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    assignment = db.Column(db.Integer, db.ForeignKey('assignments.id'))
    grade = db.Column(db.Integer)
    dategraded = db.Column(db.DateTime)
    
    assignmentR = db.relationship('Assignments', backref='grades', lazy=True)
   
    def __repr__(self):
        return f'assignment: {self.assignment}, grade: {self.grade}, dategraded: {self.dategraded}'
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "assignment": self.assignment,
            "grade": self.grade,
            "dategraded": self.dategraded
        }
    
    
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
    
    def to_dict(self):
        parsed_submission = get_dict_from_string(self.submission) if self.submission[0] == '{'  else self.submission
        if 'abi' in parsed_submission:
            parsed_submission['abi'] = get_dict_from_string(parsed_submission['abi'])
        return {
            "id": self.id,
            "user_id": self.user_id,
            "assignment": self.assignment,
            "submission": parsed_submission,
            "date_submitted": self.date_submitted,
            "grade": self.grade,
            "comment": self.comment
        }
    
class Quiz_Header(db.Model):
    __tablename__ = 'quiz_header'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    multiple_retries = db.Column(db.Boolean)
    grade_category = db.Column(db.String(50))
    active = db.Column(db.Boolean)

    duedates = db.relationship('Quiz_DueDates', backref='quiz', lazy='joined')
    topics = db.relationship('Quiz_Topics', backref='quiz', lazy='joined')
    
    def __repr__(self):
        return f'id: {self.id} description: {self.description} multiple retires {self.multiple_retries} active {self.active}'
    
    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "multiple_retries": self.multiple_retries,
            "grade_category": self.grade_category,
            "active": self.active,
            "duedates": [duedate.to_dict() for duedate in self.duedates],
            "topics": [topic.to_dict() for topic in self.topics]
        }
    
class Quiz_DueDates(db.Model):
    __tablename__ = 'quiz_duedates'
    id = db.Column(db.Integer, primary_key=True)
    quiz_header = db.Column(db.Integer, db.ForeignKey('quiz_header.id'))
    section = db.Column(db.Integer,db.ForeignKey('sections.id'))
    date_due = db.Column(db.DateTime)

    sectioninfo = db.relationship('Sections', lazy='joined')
    
    def __repr__(self):
        return f'id: {self.id} quiz_header: {self.quiz_header} section: {self.section} date due: {self.date_due}'
    
    def to_dict(self):
        return {
            "id": self.id,
            "quiz_header": self.quiz_header,
            "section_id": self.section,
            "section": self.sectioninfo.section,
            "date_due": self.date_due
        }
    
class Quiz_Topics(db.Model):
    __tablename__ = 'quiz_topics'
    id = db.Column(db.Integer, primary_key=True)
    quiz_header = db.Column(db.Integer, db.ForeignKey('quiz_header.id'))
    topic = db.Column(db.String(100))
    number_of_questions = db.Column(db.Integer)
    
    def __repr__(self):
        return f'topic {self.topic} number of questions {self.number_of_questions}'
    
    def to_dict(self):
        return {
            "id": self.id,
            "quiz_header": self.quiz_header,
            "topic": self.topic,
            "number_of_questions": self.number_of_questions
        }
    
 
class Quizzes(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    quiz_header = db.Column(db.Integer, db.ForeignKey('quiz_header.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    submitted = db.Column(db.Boolean)
    grade = db.Column(db.Integer)
    
    def __repr__(self):
        return f'quiz_header: {self.quiz_header}, user_id: {self.user_id}, submitted: {self.submitted}, grade: {self.grade}'
    
    def to_dict(self):
        return {
            "id": self.id,
            "quiz_header": self.quiz_header,
            "user_id": self.user_id,
            "submitted": self.submitted,
            "grade": self.grade
        }
    
class Questions(db.Model):
    __tablename__ = 'questions'
    question_id = db.Column(db.Integer,primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    topic = db.Column(db.String(50))
    question = db.Column(db.String(500))
    display_order = db.Column(db.Integer)
    answer_chosen = db.Column(db.Integer)
    is_correct = db.Column(db.Boolean)
    
    def __repr__(self):
        return f'id: {self.question_id} topic: {self.topic}  question: {self.question} display order: {self.display_order} answer chosen: {self.answer_chosen} correct: {self.is_correct}'
    
    def to_dict(self):
        return {
            "question_id": self.question_id,
            "quiz_id": self.quiz_id,
            "topic": self.topic,
            "question": self.question,
            "display_order": self.display_order,
            "answer_chosen": self.answer_chosen,
            "is_correct": self.is_correct
        }
    
class Answers(db.Model):
    __tablename__ = 'answers'
    answer_id = db.Column(db.Integer,primary_key=True)
    question_id = db.Column(db.Integer,db.ForeignKey('questions.question_id'))
    display_order = db.Column(db.Integer)
    answer_txt = db.Column(db.String(100))
    correct_answer = db.Column(db.Boolean)
    
    def __repr__(self):
        return f'id: {self.answer_id}, Display Order: {self.display_order}, Text: {self.answer_txt}, Correct Answer? :{self.correct_answer}'
    
    def to_dict(self):
        return {
            "answer_id": self.answer_id,
            "question_id": self.question_id,
            "display_order": self.display_order,
            "answer_txt": self.answer_txt,
            "correct_answer": self.correct_answer
        }
    

    
class QuestionBank(db.Model):
    __tablename__ = 'question_bank'
    question_id = db.Column(db.Integer,primary_key=True)
    topic = db.Column(db.String(50))
    question = db.Column(db.String(500))
    
    def __repr__(self):
        return f'id: {self.question_id} topic: {self.topic}  question: {self.question} '
    
    def to_dict(self):
        return {
            "question_id": self.question_id,
            "topic": self.topic,
            "question": self.question
        }
    
class AnswerBank(db.Model):
    __tablename__ = 'answer_bank'
    answer_id = db.Column(db.Integer,primary_key=True)
    question_id = db.Column(db.Integer,db.ForeignKey('questions.question_id'))
    answer_txt = db.Column(db.String(100))
    correct_answer = db.Column(db.Boolean)
    
    def __repr__(self):
        return f'id: {self.answer_id}, Text: {self.answer_txt}, Correct Answer? :{self.correct_answer}'
    
    def to_dict(self):
        return {
            "answer_id": self.answer_id,
            "question_id": self.question_id,
            "answer_txt": self.answer_txt,
            "correct_answer": self.correct_answer
        }
    
class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    # description = db.Column(db.String(50))
    
    def __repr__(self):
        return f'user_id: {self.user_id} date: {self.date.strftime("%m/%d/%Y %H:%M")}'
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "date": self.date.strftime("%m/%d/%Y %H:%M")
        }