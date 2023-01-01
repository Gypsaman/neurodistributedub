from flask import Blueprint,render_template,request
from flask_login import current_user
from webproject.models import User,Wallet,Transactions
from webproject.web3_interface import  getEthTrans
from webproject.table_creator import table_creator
from webproject import db

from flask_login import login_required


trans = Blueprint('trans',__name__)

@trans.route('/transactions/<int:page_num>')
def transactions(page_num):
    items_per_page = 15
    transactions = Transactions.query.filter_by(user_id=current_user.id).all()

    table = table_creator('Transactions',transactions,items_per_page,page_num,actions=['View'])
    
    return render_template('trans/transactions.html',table=table)

@trans.route('/transactions/view/<int:page_num>/<int:tran_id>')
def transactions_view(page_num,tran_id):
    transaction = Transactions.query.filter_by(id=tran_id).first()
    return render_template('/trans/view_transaction.html',transaction=transaction,page_num=page_num)

@trans.route('/addethtransactions')
@login_required
def add_eth_transaction():
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    trans = getEthTrans(wallet.wallet)
    for tran in trans:
        tran['user_id'] = current_user.id
        tran['wallet'] = wallet.wallet
        exists = Transactions.query.filter_by(hash=tran['hash']).first()
        if exists:
            continue
        transaction = Transactions(**tran)
        db.session.add(transaction)
        db.session.commit()
    return render_template('trans/transactions.html')
