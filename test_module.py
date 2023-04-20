from webproject.modules.offline_utils import grade_history_data
from webproject.modules.quizzes import create_quiz_all_users, Topics, create_quiz, create_final
from webproject import db, create_app
from webproject.models import Quizzes, User,Assignments, Submissions, Grades
from graders.check_submissions import check_submissions
from datetime import datetime,timedelta
import json
import csv
from graders.final_grade import publish_final_grades, letter_grades


grades = publish_final_grades()
with open('./xtesting/final_grades.csv','w') as f:
    writer = csv.writer(f)
    writer.writerow(grades[0].keys())
    for grade in grades:
        writer.writerow(grade.values())
        


# with create_app().app_context():
#     quizzes = Quizzes.query.all()
#     json_quizzes = {}
#     for quiz in quizzes:
#         desc = quiz.description[:quiz.description.find('for')-1]
#         if desc == 'Web3 Quiz':
#             desc = 'Web3'
#         if desc == 'Tokens':
#             desc = 'Token'
#         if desc not in json_quizzes:
#             json_quizzes[desc] = {'date_available':quiz.date_available.strftime('%Y-%m-%d %H:%M:%S'),
#                                   'date_due':quiz.date_due.strftime('%Y-%m-%d %H:%M:%S'),
#                                   'multiple_retries':quiz.multiple_retries,
#                                   'active':quiz.active,'quizzes':[quiz.id]}
#         else:
#             json_quizzes[desc]['quizzes'].append(quiz.id)

#     with open('quizzes.json','w') as f:
#         json.dump(json_quizzes,f)
