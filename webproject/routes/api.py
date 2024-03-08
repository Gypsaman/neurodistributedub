from webproject.routes import admin_required
from flask import Blueprint, render_template
from webproject.models import Submissions
import json

api = Blueprint("api", __name__)


@api.route("/api/submissions")
@admin_required
def submissions():
    submissions = []
    for submission in Submissions.query.filter_by(assignment=4).all():
        submissions.append(submission.to_dict())
    return submissions
    

