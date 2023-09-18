from webproject.modules.create_initial_data import create_initial_data,send_new_user_email
from webproject.modules.quizzes import create_quiz, create_quiz_all_users
from datetime import datetime as dt
from datetime import timedelta
from webproject.models import User,Sections,Quiz_Header,Quiz_Topics, Quizzes,Questions, Answers
from webproject import db, create_app
from webproject.modules.dotenv_util import load_dotenv
from webproject.modules.quizzes import Topics
from graders.check_submissions import check_submissions
import pandas as pd

# check_submissions()
load_dotenv()


# create_initial_data()
# df = pd.read_csv('data/rosters/FA23-Thursday.csv')

load_dotenv()

def delete_quizzes():
    for ans in Answers.query.all():
        db.session.delete(ans)
    for q in Questions.query.all():
        db.session.delete(q)
    for quiz in Quizzes.query.all():
        db.session.delete(quiz)
    for topic in Quiz_Topics.query.all():
        db.session.delete(topic)
    for header in Quiz_Header.query.all():
        db.session.delete(header)
    db.session.commit()    


with create_app().app_context():
    delete_quizzes()
    topics_selected = {"Encryption": 9}
    quiz_id = create_quiz(
                description= "Encryption",
                date_available= dt.strptime('09/18/2023 23:59','%m/%d/%Y %H:%M'),
                date_due=dt.strptime('09/24/2023 23:59','%m/%d/%Y %H:%M'),
                topics = topics_selected,
                multiple_retries=True,
                active=True
                )
    create_quiz_all_users('FA23-Monday',quiz_id)
    
    quiz_id = create_quiz(
                description= "Encryption",
                date_available= dt.strptime('09/18/2023 23:59','%m/%d/%Y %H:%M'),
                date_due=dt.strptime('09/24/2023 23:59','%m/%d/%Y %H:%M'),
                topics = topics_selected,
                multiple_retries=True,
                active=True
                )
    create_quiz_all_users('FA23-Thursday',quiz_id)

    topics_selected = {"Blockchain": 7}
    quiz_id = create_quiz(
                description= "BlockChain",
                date_available= dt.strptime('09/18/2023 23:59','%m/%d/%Y %H:%M'),
                date_due=dt.strptime('09/24/2023 23:59','%m/%d/%Y %H:%M'),
                topics = topics_selected,
                multiple_retries=True,
                active=True
                )
    create_quiz_all_users('FA23-Monday',quiz_id)
    
    
    quiz_id = create_quiz(
                description= "BlockChain",
                date_available= dt.strptime('09/18/2023 23:59','%m/%d/%Y %H:%M'),
                date_due=dt.strptime('09/24/2023 23:59','%m/%d/%Y %H:%M'),
                topics = topics_selected,
                multiple_retries=True,
                active=True
                )
    create_quiz_all_users('FA23-Thursday',quiz_id)


with create_app().app_context():
    for quiz in Quizzes.query.all():
        print(quiz)
        
