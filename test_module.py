from dbutilities.create_initial_data import create_initial_data,send_new_user_email
from webproject.modules.quizzes import create_quiz, create_quiz_all_users
from datetime import datetime as dt
from datetime import timedelta
from webproject.models import User,Sections,Quiz_Header,Quiz_Topics, Quizzes,Questions, Answers
from webproject import db, create_app
from webproject.modules.dotenv_util import load_dotenv

load_dotenv()

# create_initial_data()
with create_app().app_context():
    
    # topics_selected = {"NFT": 11}
    # quiz_id = create_quiz(
    #             description= "NFT Quiz",
    #             date_available= dt.now(),
    #             date_due= dt.now()+timedelta(days=7),
    #             topics = topics_selected,
    #             multiple_retries=True,
    #             active=True
    #             )
    # create_quiz_all_users('FA23-Monday',quiz_id)

    
    for user in User.query.all():
        print(user)
        
    # for section in Sections.query.all():
    #     print(section)
    # quizzes = db.session.query(Quizzes,Quiz_Header).join(Quiz_Header).filter(Quizzes.user_id==2).all()
    # for quiz in quizzes:
    #     print(quiz.description)

    # for quiz in Quiz_Header.query.all():
    #     print(quiz)
    #     for topic in Quiz_Topics.query.filter_by(quiz_header=quiz.id).all():
    #         print(topic)

    # for quiz in Quizzes.query.all():
    #     print(quiz)
        # for question in Questions.query.filter_by(quiz_id=quiz.id).all():
        #     print(question)
        #     for answer in Answers.query.filter_by(quiz_id=quiz.id,question_id=question.question_id):
        #         print(answer)

        

