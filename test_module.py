from webproject import create_app, db
from webproject.models import QuestionBank,AnswerBank, Questions, Quiz_Topics, Quiz_Header, Quizzes, Answers
import json
from webproject import create_app, db
from webproject.modules.offline_utils import email_course_evaluation
from graders.check_submissions import check_submissions


check_submissions()