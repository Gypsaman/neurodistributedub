from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from webproject import db
from webproject.models import Assignments, DueDates, Grades, Submissions, User, Sections
from webproject.modules.table_creator import Field, TableCreator, timestamp_to_date
from webproject.routes import admin_required
from datetime import datetime as dt

quiz = Blueprint("quiz", __name__)

@quiz.route("/quiz")
@admin_required
def quiz_display():
    pass