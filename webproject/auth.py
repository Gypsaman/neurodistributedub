from flask import Blueprint,render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user, login_required, logout_user
from . import db

auth = Blueprint('auth',__name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login',methods=['POST'])
def login_post():
    
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False



    curr_usr = User.query.filter_by(email=email).first()

    if not curr_usr or not check_password_hash(curr_usr.password,password):
        flash('Incorrect email/password combination')
        return redirect(url_for('auth.login'))
    login_user(curr_usr,remember=remember)
    return redirect(url_for('main.welcome'))


@auth.route('/register')
def register():
    return render_template('register.html')


@auth.route('/register',methods=['POST'])
def register_post():
    email = request.form.get('email')
    first_name = request.form.get('firstname')
    last_name = request.form.get('lastname')
    student_id = request.form.get('studentid')
    password = request.form.get('password')

    curr_User = User.query.filter_by(email=email).first()

    if curr_User:
        flash('Email exists already')
        return redirect(url_for('auth.register'))

    new_usr = User(email=email,first_name=first_name,last_name=last_name,student_id=student_id, password=generate_password_hash(password,method='sha256'))

    db.session.add(new_usr)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))