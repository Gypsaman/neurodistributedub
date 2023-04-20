from webproject.models import Grades,Quizzes,User,Assignments
from webproject import db, create_app
from webproject.modules.ubemail import UBEmail

letter_grades = {'A':(94.9,100),'A-':(90,94.8),'B+':(87,89.9),'B':(83,86.9),'B-':(80,82.9),'C+':(77,79.9),'C':(73,76.9),'C-':(70,72.9),'D+':(67,69.9),'D':(63,66.9),'D-':(60,62.9),'F':(0,59.9)}

midterm_assignment = "  Mid Term"
midterm_quiz = "Mid Term Quiz"
final_assignment = "Final Project"
final_quiz = "Final"
extra_credit = 'ECC Curve'

additional_extra_credit = ['1181220','1179119']

def get_letter_grade(score):
    score = round(score,1)
    for key,value in letter_grades.items():
        if score >= value[0] and score <= value[1]:
            return key
    return 'F'

def final_grades_student(id):
    with create_app().app_context():
        user = User.query.filter_by(id=id).first()
    
        grades = {'Assignments':[],'Midterms':[],'Finals':[],'Extra Credit':[]}
        assignments = Assignments.query.all()
        for assignment in assignments:
            grade = Grades.query.filter_by(user_id=id,assignment=assignment.id).first()
            score = 0 if grade is None else grade.grade
            if assignment.name in [midterm_assignment,midterm_quiz]:
                grades['Midterms'].append((assignment.name,score,score/100*15 ))
            elif assignment.name == final_assignment:
                grades['Finals'].append((assignment.name,score,score/100*10 ))
            elif assignment.name == extra_credit:
                grades['Extra Credit'].append((assignment.name,score,2 if score > 0 else 0))
            else:
                grades['Assignments'].append((assignment.name,score,score/1600*40 ))
        if user.student_id in additional_extra_credit:
            grades['Extra Credit'].append(('Additional Extra Credit',score,2))
        quizzes = Quizzes.query.filter_by(user_id=id).all()
        for quiz in quizzes:
            score = 0 if quiz.grade is None else quiz.grade
            if quiz.description.split(' ')[0] == midterm_quiz:
                grades['Midterms'].append((quiz.description,score,score/100*15))
            elif quiz.description.split(' ')[0] == final_quiz:
                grades['Finals'].append((quiz.description,score,score/100*20))
            else:
                grades['Assignments'].append((quiz.description,score,score/1600*40))
        return grades
        
def publish_final_grades():
    grades = []
    with create_app().app_context():
        for user in User.query.filter_by(role='student').all():
            final_grades = final_grades_student(user.id)
            msg,grade = build_grade_message(final_grades,user,type='Preview')
            # email = UBEmail()
            # email.send_email(user.email,'Final Grades Preview',msg)
            grades.append({"id":user.id,"grade":grade,"Letter_grade":get_letter_grade(grade),"student_id":user.student_id,"first_name":user.first_name,"last_name":user.last_name,"email":user.email})
    
    return grades
            
            
            
def build_grade_message(final_grades, user, type='FINAL'):
    msg = f'Hello {user.first_name} ({user.student_id})\n\n'
    if type == 'Preview':
        msg += 'This is a preview of your final grade.\n'
        msg += 'Final Grades are due on Monday April 24\n'
        msg += 'Please let me know if I have made any mistakes.\n\n'
    msg += 'As a reminder, the final grade is calculated as follows:\n'
    msg += 'Assignments and Quizzes: 40%\n'
    msg += 'Midterm: 30%\n'
    msg += 'Final: 30%\n\n'
    
    msg += f'Your grades are as follows:\n\n'
    
    overall_total = 0
    for type,grades in final_grades.items():
        msg = msg + type+'\n'
        msg = msg + '-'*len(type)+'\n'
        type_total = 0
        for grade in grades:
            msg += f'{grade[0].strip()}: {grade[1]:.2f}\n'
            type_total += grade[2]
        msg += f'\nGrade: {type_total:.2f}%\n\n'
        overall_total += type_total
    msg += f'FINAL GRADE: {min(overall_total,100):.2f}'
    return msg,overall_total