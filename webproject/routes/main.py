from flask import Blueprint,render_template,request,redirect,flash,url_for,send_from_directory
from flask_login import current_user
from webproject.routes import admin_required
from webproject.models import User,Wallet,Assignments,Grades, Attendance
from webproject.modules.web3_interface import get_eth_balance
from webproject.classdocs.content import content
from webproject import db
from flask_login import login_required
from datetime import datetime as dt
import hashlib
import os
from flask import jsonify
from sqlalchemy import text
import json 
from graders.MidTermExam import email_exams


main = Blueprint('main',__name__)

def email_midtermexam():
    if not Assignments.query.filter_by(name='Mid Term').first().active:
        return
    exam_distribution = json.load(open('/var/www/dna/graders/exam_distribution.json','r'))
    exam_data = exam_distribution[current_user.student_id]
    if exam_data['emailed']:
        return

    email_exams(current_user.section,current_user.student_id)
    exam_distribution[current_user.student_id]['emailed'] = True
    json.dump(exam_distribution,open('/var/www/dna/graders/exam_distribution.json','w'))

@main.route('/environment')
def environment():

    return f'{os.listdir()}'

@main.route('/AttendanceCodeValue')
@admin_required
def attendance_code_value():
    date = dt.strftime(dt.now(),'%Y-%m-%d %H:%M:%S')[:-1]
    code = hashlib.sha256(date.encode()).hexdigest()[:5]
    today = dt.today().date()
    date_format = "%Y-%m-%d"

    stmt = "SELECT user.id, date FROM user  left join "
    stmt += f"(select user_id, max(date) as date from attendance where date > '{today.strftime(date_format)}' group by user_id) as att "
    stmt += "on user.id = user_id where date is null and user.role = 'student'"

    users = list(db.session.execute(text(stmt)))
    return jsonify({'code':code,'NotAttended':len(users)})

@main.route('/attendance_code')
@admin_required
def attendance_code():
    return render_template('main/attendance_code.html')

@main.route('/attendance')
@login_required
def attendance():
    return render_template('main/attendance.html')

@main.route('/attendance',methods=["POST"])
@login_required
def attendance_post():
    code = request.form.get('attendance_code')

    date = dt.strftime(dt.now(),'%Y-%m-%d %H:%M:%S')[:-1]
    hash = hashlib.sha256(date.encode()).hexdigest()[:5]
    if code != hash:
        flash(f'Incorrect Attendance Code!{code}')
        return redirect(url_for('main.attendance'))
    attendance = Attendance(user_id=current_user.id,date=dt.now())
    db.session.add(attendance)
    db.session.commit()
    # email_midtermexam()
    return redirect(url_for('dashb.dashboard'))

@main.route('/')
def index():
    return render_template('main/index.html')

@main.route('/resources/<class_name>')
@login_required
def resources(class_name):
    slides = content[class_name]['slides']+content[class_name]['resources']
    videos = content[class_name]['videos']
    return render_template('main/resources.html',slides=slides,videos=videos,class_name=class_name)

@main.route('/resources/select')
@login_required
def resources_select():
    classes = content.keys()
    return render_template('main/resources_select.html',classes=classes )

@main.route('/resources/select',methods=['POST'])
@login_required
def resources_select_post():
    class_name = request.form['class']
    return redirect(url_for('main.resources',class_name=class_name))

@main.route('/resources/slides/<path:filename>')
@login_required
def view_slides(filename):
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return send_from_directory(os.path.join(current_dir,'classdocs/files'),filename)

@main.route('/resources/videos/<path:filename>')
@login_required
def view_videos(filename):
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return send_from_directory(os.path.join(current_dir,'classdocs/files'),filename)

@main.route('/wallet')
@login_required
def wallet():
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    return render_template('main/wallet.html',wallet=wallet)

def verify_wallet(wallet_address):
    
    
    if Wallet.query.filter_by(wallet=wallet_address).first() is not None:
        return False, 'Wallet already in use'
    
    eth_balance = get_eth_balance(wallet_address)

    if eth_balance == -1:
        return False, 'Invalid wallet address'
    
    if eth_balance == 0:
        return False, 'Wallet address has no ETH'
    
    return True, 'Wallet address is valid'
        
        
@main.route('/wallet',methods=["POST"])
@login_required
def wallet_post():

    wallet_address = request.form.get('walletaddress')
    
    valid, msg = verify_wallet(wallet_address)
    
    if not valid:
        flash(msg)
        return redirect(url_for('main.wallet'))
    
    wallet = Wallet(wallet=wallet_address,user_id=current_user.id)
    assignment = Assignments.query.filter_by(name='Wallet').first()
    grade = Grades(user_id=current_user.id,assignment=assignment.id,grade=100,dategraded=dt.now())    
    
    db.session.add(grade)
    db.session.add(wallet)
    db.session.commit()
    
    return redirect(url_for('dashb.dashboard'))

@main.route('/wallet/update/<int:wallet_id>',methods=["GET","POST"])
def wallet_update(wallet_id):
    wallet = Wallet.query.filter_by(id=wallet_id).first()
    if request.method == "POST":
        wallet_addr = request.form['wallet_address']
        valid, msg = verify_wallet(wallet_addr)

        if not valid:
            flash(msg)
            return redirect(url_for('main.wallet_update',wallet_id=wallet_id))
        wallet.wallet = wallet_addr
        db.session.commit()
        return redirect(url_for('dashb.dashboard'))
    
    return render_template('main/wallet_update.html',wallet=wallet)


@main.route('/welcome')
@login_required
def welcome():
    return render_template('main/welcome.html',first_name=current_user.first_name,last_name=current_user.last_name)



@main.route('/profile')
@login_required
def profile():

    usr_email = current_user.email
    curr_usr = User.query.filter_by(email=usr_email).first()
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    tokens = 0
    nfts = 0
    
    eth_balance = f'{get_eth_balance(wallet.wallet):0.4f}' if wallet else 0
    
    return render_template('main/profile.html',user=curr_usr,wallet=wallet,tokens=tokens,nfts=nfts,eth_balance=eth_balance)





