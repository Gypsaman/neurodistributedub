from webproject.models import Grades,Quizzes,Quiz_Header,User,Assignments
from webproject import db, create_app
from webproject.modules.ubemail import UBEmail

letter_grades = {'A':(94.9,100),'A-':(90,94.8),'B+':(87,89.9),'B':(83,86.9),'B-':(80,82.9),'C+':(77,79.9),'C':(73,76.9),'C-':(70,72.9),'D+':(67,69.9),'D':(63,66.9),'D-':(60,62.9),'F':(0,59.9)}


additional_extra_credit = []
grade_portion = {'Assignment':40/1600,'Midterm':15,'Final':15,'Extra Credit':2}

def get_letter_grade(score):
    score = round(score,1)
    for key,value in letter_grades.items():
        if score >= value[0] and score <= value[1]:
            return key
    return 'F'

def final_grades_student(id):
    user = User.query.filter_by(id=id).first()

    grades = {'Assignment':{},'Midterm':{},'Final':{},'Extra Credit':{}}
    assignments = Assignments.query.all()
    for assignment in assignments:
        grade = Grades.query.filter_by(user_id=id,assignment=assignment.id).first()
        score = 0 if grade is None else max(0,grade.grade)
        
        grades[assignment.grade_category][assignment.name] = {
            "score":score,
            "grade_portion":score/grade_portion[assignment.grade_category]
            }

    if user.student_id in additional_extra_credit:
        grades['Extra Credit'].append(('Additional Extra Credit',score,2))
    quizzes = Quizzes.query.filter_by(user_id=id).all()
    for quiz in quizzes:
        header = Quiz_Header.query.filter_by(id=quiz.quiz_header).first()
        score = 0 if quiz.grade is None else quiz.grade
        grades[header.grade_category][f'{header.description}-Quiz'] = {"score":score,"grade_portion":score/grade_portion[header.grade_category]}

    return grades

      
def publish_final_grades(type='Preview',email=False):
    grades = []

    with create_app().app_context():
        for user in User.query.filter_by(role='student').all():
            final_grades = final_grades_student(user.id)
            msg,grade = build_grade_message(final_grades,user,type=type)
            if email:
                email = UBEmail()
                email.send_email(user.email,'Final Grades Preview',msg)
            grades.append({"id":user.id,
                           "grade":grade,
                           "Letter_grade":get_letter_grade(grade),
                           "student_id":user.student_id,
                           "first_name":user.first_name,
                           "last_name":user.last_name,
                           "email":user.email,
                           "section":user.section})
    
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
            msg += f"{grade.strip()}: {grades[grade]['score']:.1f}\n"
            type_total += grades[grade]['grade_portion']
        msg += f'\nGrade: {type_total:.2f}%\n\n'
        overall_total += type_total
    overall_total = min(overall_total,100)
    msg += f'FINAL GRADE: {overall_total:.1f} ({get_letter_grade(overall_total)})'
    return msg,overall_total

def course_evaluation_email():
    with create_app().app_context():
        users = User.query.filter_by(role='student').all()
        for user in users:
            msg = f'Hello {user.first_name.title()},\n\n'
            msg += "I want to thank you for participating in the course this semester. I hope you found the course interesting and useful. If you haven't done so already, I would like to ask you to take a few minutes to fill out a course evaluation. The course evaluation is anonymous and will help me improve the course for future semesters.\n\n"
            msg += 'Thank you\n\nCesar Garcia'
            email = UBEmail()
            email.send_email(user.email,'Course Evaluation',msg)