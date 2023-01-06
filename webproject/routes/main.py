from flask import Blueprint,render_template,request,redirect,flash,url_for
from flask_login import current_user
from webproject.models import User,Wallet,Assets,Transactions,Assignments,Grades
from webproject.modules.web3_interface import get_eth_balance
from webproject.modules.table_creator import table_creator
from webproject import db
from flask_login import login_required


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
def wallet_post():

    wallet_address = request.form.get('wallet_address')
    private_key = request.form.get('private_key')
    if not wallet_address or not private_key:
        flash('Please fill all the fields')
        return redirect(url_for('main.wallet'))
    curr_wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    if curr_wallet:
        flash('Wallet already exists')
        return redirect(url_for('main.wallet'))
    wallet = Wallet(wallet=wallet_address,privatekey=private_key,user_id=current_user.id)
    
    db.session.add(wallet)
    db.session.commit()
    
    return redirect(url_for('main.profile'))

@main.route('/welcome')
def welcome():
    return render_template('main/welcome.html',first_name=current_user.first_name,last_name=current_user.last_name)



@main.route('/tokens')
def tokens():
    return render_template('main/tokens.html')


@main.route('/profile')
def profile():

    usr_email = current_user.email
    curr_usr = User.query.filter_by(email=usr_email).first()
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    tokens = Assets.query.filter_by(user_id=curr_usr.id, asset_type=1).count()
    nfts = Assets.query.filter_by(user_id=curr_usr.id, asset_type=2).count()
    
    eth_balance = f'{get_eth_balance(wallet.wallet):0.4f}' if wallet else 0
    
    return render_template('main/profile.html',user=curr_usr,wallet=wallet,tokens=tokens,nfts=nfts,eth_balance=eth_balance)





