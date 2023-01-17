from flask import Blueprint,render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from webproject.models import User, PasswordReset
from flask_login import login_user, logout_user, current_user
from webproject import db
from flask_login import login_required
from webproject.routes import admin_required
from datetime import datetime as dt
import random
from webproject.modules.ubemail import UBEmail
from webproject.modules.table_creator import TableCreator, Field

auth = Blueprint('auth',__name__)



@auth.route('/login')
def login():
    return render_template('auth/login.html')

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
    return redirect(url_for('dashb.dashboard'))


@auth.route('/register')
def register():
    return render_template('auth/register.html')


@auth.route('/register',methods=['POST'])
def register_post():
    
    email =  request.form.get('email')
    curr_User = User.query.filter_by(email=email).first()

    if curr_User:
        flash('Email exists already')
        return redirect(url_for('auth.register'))
    
    curr_user = User.query.filter_by(student_id=request.form.get('studentid')).first()
    if curr_user:
        flash('Student ID exists already')
        return redirect(url_for('auth.register'))
    
    record = {
        'email': email,
        'first_name' : request.form.get('firstname'),
        'last_name' : request.form.get('lastname'),
        'student_id' : request.form.get('studentid'),
        'password' : generate_password_hash(request.form.get('password'),method='sha256'),
        'role'  : 'admin' if email=='gypsaman@gmail.com' else 'student'
    }
    
    new_usr = User(**record)

    db.session.add(new_usr)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/passwordreset', methods=['GET','POST'])
def password_reset():
    if request.method == "POST":
        
        user = User.query.filter_by(email=request.form.get('email')).first()
        
        if not user:
            flash('Email does not exist')
            return redirect(url_for('auth.password_reset'))
        
        existing_pwdreset = PasswordReset.query.filter_by(user_id=user.id).first()
        if existing_pwdreset:
            db.session.delete(existing_pwdreset)    
            db.session.commit()
            
            
        password_phrase = random.randint(100000,999999)
        phrase_expires = dt.now().replace(minute=dt.now().minute+5)
                
        pwdreset = PasswordReset(user_id=user.id,password_phrase=password_phrase,phrase_expires=phrase_expires)
        
        db.session.add(pwdreset)
        db.session.commit()
        
        email = UBEmail()
        body = f'Your password reset link is http://neurodistributed.com/passwordupdate/{password_phrase}'
        body += f'\n\nThis link will expire in 5 minutes'
        
        email.send_email(user.email,'Password Reset',body)
        
        flash('Password reset link has been sent to your email')
        
        return redirect(url_for('auth.login'))
    return render_template('auth/password_reset.html')



@auth.route('/passwordupdate/<int:id>')
def password_update(id):
    pwdreset = PasswordReset.query.filter_by(password_phrase=id).first()
    if not pwdreset or dt.now() > pwdreset.get_password_phrase_expiry():
        flash('You are not authorized to update the password')
        # flash(f'{id} {dt.now()}')
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(id=pwdreset.user_id).first()
    return render_template('auth/update_password.html',user=user,pwdreset=pwdreset)

@auth.route('/passwordupdate/<int:id>',methods=['POST'])
def password_update_post(id):
    if request.form.get('new_password') != request.form.get('confirm_password'):
        flash('Passwords do not match')
        return redirect(url_for('auth.password_update',id=id))
    pwdreset = PasswordReset.query.filter_by(password_phrase=id).first()
    user = User.query.filter_by(id=pwdreset.user_id).first()
    user.password = generate_password_hash(request.form.get('new_password'),method='sha256')

    db.session.delete(pwdreset)
    
    db.session.commit()
    
    return redirect(url_for('auth.login'))

