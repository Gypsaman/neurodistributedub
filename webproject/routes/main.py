from flask import Blueprint,render_template,request,redirect,flash,url_for
from flask_login import current_user
from webproject.models import User,Wallet,Assets,Assignments,Grades, Attendance
from webproject.modules.web3_interface import get_eth_balance
from webproject import db
from flask_login import login_required
from datetime import datetime as dt
import hashlib


main = Blueprint('main',__name__)


@main.route('/attendance')
@login_required
def attendance():
    return render_template('main/attendance.html')

@main.route('/attendance',methods=["POST"])
@login_required
def attendance_post():
    code = request.form.get('attendance_code')
    if dt.strftime(dt.now(),"%M") > '20':
        flash('Attendance code expired!')
        return redirect(url_for('main.attendance'))
    date = dt.strftime(dt.now(),'%Y-%m-%d') 
    if code != hashlib.sha256(date.encode()).hexdigest()[:5]:
        flash('Incorrect Attendance Code!')
        return redirect(url_for('main.attendance'))
    attendance = Attendance(user_id=current_user.id,date=dt.now())
    db.session.add(attendance)
    db.session.commit()
    return redirect(url_for('dashb.dashboard'))
@main.route('/')
def index():
    return render_template('main/index.html')

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
    tokens = Assets.query.filter_by(user_id=curr_usr.id, asset_type=1).count()
    nfts = Assets.query.filter_by(user_id=curr_usr.id, asset_type=2).count()
    
    eth_balance = f'{get_eth_balance(wallet.wallet):0.4f}' if wallet else 0
    
    return render_template('main/profile.html',user=curr_usr,wallet=wallet,tokens=tokens,nfts=nfts,eth_balance=eth_balance)





