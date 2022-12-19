from flask import Blueprint,render_template,request,redirect,flash,url_for
from flask_login import login_required,current_user
from .models import User,Wallet,Assets
from .web3_interface import get_eth_balance 
from . import db

main = Blueprint('main',__name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/wallet')
@login_required
def wallet():
    wallet = Wallet.query.filter_by(student_id=current_user.student_id).first()
    return render_template('wallet.html',wallet=wallet)

@main.route('/wallet',methods=["POST"])

def wallet_post():

    wallet_address = request.form.get('wallet_address')
    private_key = request.form.get('private_key')
    if not wallet_address or not private_key:
        flash('Please fill all the fields')
        return redirect(url_for('main.wallet'))
    curr_wallet = Wallet.query.filter_by(student_id=current_user.student_id).first()
    if curr_wallet:
        flash('Wallet already exists')
        return redirect(url_for('main.wallet'))
    wallet = Wallet(wallet=wallet_address,privatekey=private_key,student_id=current_user.student_id)
    
    db.session.add(wallet)
    db.session.commit()
    
    return redirect(url_for('main.profile'))

@main.route('/welcome')
def welcome():
    return render_template('welcome.html',first_name=current_user.first_name,last_name=current_user.last_name)


# Asset Management
@main.route('/assets')
@login_required
def assets():
    assets = Assets.query.filter_by(student_id=current_user.student_id).all()
    return render_template('assets.html',assets=assets)

@main.route('/assetdelete/<int:id>')
def assets_delete(id):
    addr = id
    asset_to_delete = Assets.query.get_or_404(id)
    try:
        db.session.delete(asset_to_delete)
        db.session.commit()
        return redirect('/assets')
    except:
        flash("There was a problem deleting the asset")
        return redirect('/assets')
        

@main.route('/addassets')
@login_required
def add_assets():
    return render_template('addassets.html')

@main.route('/addassets',methods=["POST"])
@login_required
def add_assets_post():
    student_id = current_user.student_id
    asset_type = request.form.get('asset_type')
    network = request.form.get('network')
    asset_address   = request.form.get('asset_address')
    
    asset_exists = Assets.query.filter_by(asset_address=asset_address).first()
    if asset_exists:
        flash('Asset already exists')
        return redirect(url_for('main.assets'))
    
    asset = Assets(student_id=student_id,asset_type=asset_type,network=network,asset_address=asset_address)
    
    db.session.add(asset)
    db.session.commit()
    
    return redirect(url_for('main.profile'))


@main.route('/tokens')
def tokens():
    return render_template('tokens.html')

@main.route('/transactions')
def transactions():
    return render_template('transactions.html')



@main.route('/profile')
def profile():
    usr_email = current_user.email
    curr_usr = User.query.filter_by(email=usr_email).first()
    wallet = Wallet.query.filter_by(student_id=curr_usr.student_id).first()
    tokens = Assets.query.filter_by(student_id=curr_usr.student_id, asset_type=1).count()
    nfts = Assets.query.filter_by(student_id=curr_usr.student_id, asset_type=2).count()
    eth_balance = f'{get_eth_balance(wallet.wallet):0.4f}'
    return render_template('profile.html',user=curr_usr,wallet=wallet,tokens=tokens,nfts=nfts,eth_balance=eth_balance)
