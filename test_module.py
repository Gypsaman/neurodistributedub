from webproject import create_app, db
from webproject.models import QuestionBank,AnswerBank, Questions, Quiz_Topics, Quiz_Header, Quizzes, Answers
import json
from webproject import create_app, db
from webproject.modules.offline_utils import email_course_evaluation
from graders.check_submissions import check_submissions
from webproject.models import User,Quiz_Header, Quizzes, Submissions, Assignments
from collections import Counter
from graders.grade_final import gradeFinal
from webproject.modules.grading import build_grades,publish_final_grades
# check_submissions()
with create_app().app_context():
    # build_grades()
    publish_final_grades(type='Final',email=True)
    # assgn = Assignments.query.filter_by(id=13).first()
    # data = []
    # for sub in Submissions.query.filter_by(assignment=assgn.id).all():
    #     if 'build/contracts' in sub.comment:
    #         try:
    #             grade,msg = gradeFinal(f'E:\\Teaching\\CPS-570 BlockChain\\2023 Fall\\uploads_history\\{sub.submission}')
    #             print(sub.user_id,grade,msg)
    #         except Exception as e:
    #             print(sub.user_id)
                


