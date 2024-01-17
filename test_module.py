from webproject import create_app, db
from webproject.models import User, Grades, Quizzes

with create_app().app_context():
    results = {}
    for user in User.query.filter_by(section=2).all():
        grades = {}
        for grade in Grades.query.filter_by(user_id=user.id).all():
            grades[grade.assignment] = grade.grade
            for quiz in Quizzes.query.filter_by(user_id=user.id).all():
                if quiz.grade:
                    grades[quiz.quiz_header] = quiz.grade
        results[user.student_id] = grades
for student_id, grades in results.items():
    print(student_id, grades)
        

    
    

    




