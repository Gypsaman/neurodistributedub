from webproject.modules.offline_utils import grade_history_data
from webproject.modules.quizzes import create_quiz_all_users, Topics, create_quiz, create_final
from webproject import db, create_app
from webproject.models import Quizzes, User,Assignments, Submissions
from graders.check_submissions import check_submissions
from datetime import datetime,timedelta


if __name__ == '__main__':
    pt = grade_history_data()
    pt.to_excel('gradehistory.xlsx')