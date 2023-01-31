from flask import Blueprint,render_template,request,redirect,flash,url_for
from flask_login import current_user
from webproject.models import User,Wallet,Assets,Transactions,Assignments,Grades
from webproject.modules.web3_interface import get_eth_balance
from webproject import db
from flask_login import login_required
from datetime import datetime as dt


main = Blueprint('main',__name__)

@main.route('/')
def index():
    return render_template('main/index.html')

@main.route('/wallet')
@login_required
def wallet():
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    return render_template('main/wallet.html',wallet=wallet)

@main.route('/wallet',methods=["POST"])
@login_required
def wallet_post():

    wallet_address = request.form.get('wallet_address')

    
    curr_wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    if curr_wallet:
        flash('Wallet already added')
        return redirect(url_for('main.wallet'))
    
    if Wallet.query.filter_by(wallet=wallet_address).first() is not None:
        flash('Wallet already in use')
        return redirect(url_for('main.wallet'))

    if get_eth_balance(wallet_address) == 0:
        flash('Wallet address has no ETH')
        return redirect(url_for('main.wallet'))
    
    wallet = Wallet(wallet=wallet_address,user_id=current_user.id)
    assignment = Assignments.query.filter_by(name='Wallet').first()
    grade = Grades(user_id=current_user.id,assignment=assignment.id,grade=100,dategraded=dt.now())    
    
    db.session.add(grade)
    db.session.add(wallet)
    db.session.commit()
    
    return redirect(url_for('dashb.dashboard'))

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





