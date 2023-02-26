
from webproject.modules.quizzes import create_quiz
from webproject.models import Quizzes, Questions, Answers, Submissions, User, Assignments
from webproject import create_app, db
from datetime import datetime as dt
from graders.check_submissions import check_submissions

# with create_app().app_context():
#     user = User.query.filter_by(student_id='1166493').first()
#     assgn = Assignments.query.filter_by(name='Rent Car').first()
#     sub = Submissions.query.filter_by(assignment=assgn.id,user_id=user.id).first()

#     sub.grade = None
#     db.session.commit()


check_submissions()
exit()
def get_table_names():
    with create_app().app_context():
        return db.engine.table_names()
    
# print(get_table_names())

with create_app().app_context():

    topics_selected = {'Encryption': 5, 'Blockchain': 3,"Solidity": 2}
    quiz_id = create_quiz(topics_selected,description="Test",date_available=dt.strptime("2023-02-24","%Y-%m-%d"),date_due=dt.strptime("2020-01-01","%Y-%m-%d"))
    print(quiz_id)

  
    quizzes = Quizzes.query.filter_by(id=6).all()
    for quiz in quizzes:
        print(quiz.id)
        questions = Questions.query.filter_by(quiz_id=quiz.id).order_by(Questions.display_order).all()
        for question in questions:
            print(f'\t{question.display_order}-{question.question},{question.answer_chosen},{question.is_correct}')
            answers = Answers.query.filter_by(quiz_id=quiz.id,question_id=question.question_id).order_by(Answers.display_order).all()
            for answer in answers:
                print("\t\t",answer.display_order,answer.answer_txt,answer.correct_answer)
            print('*'*50)
