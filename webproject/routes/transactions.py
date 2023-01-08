from flask import Blueprint,render_template,request
from flask_login import current_user
from webproject.models import User,Wallet,Transactions
from webproject.modules.web3_interface import  getEthTrans
from webproject.modules.table_creator import TableCreator,Field,timestamp_to_date,short_hash,wei_to_eth
from webproject import db

from flask_login import login_required


trans = Blueprint('trans',__name__)

@trans.route('/transactions/<int:page_num>')
def transactions(page_num):
    fields = {
            'id': Field(None,0),
            'blockNumber': Field(None, 1),
            'timeStamp': Field(timestamp_to_date,2),
            'hash': Field(short_hash, 3),
            'nonce': Field(None, 4),
            'blockHash': Field(short_hash,5),
            'transactionIndex':Field(None, 6),
            'trans_from': Field(short_hash, 7),
            'trans_to': Field(short_hash,8),
            'value': Field(wei_to_eth, 9),
            'gas': Field(wei_to_eth, 10),
            'gasPrice': Field(wei_to_eth,11),
            'isError': Field(None,12),
            'contractAddress': Field(short_hash,13)
    }
    table_creator = TableCreator('Transactions',fields,actions=['View'])
    table_creator.set_items_per_page(15)
    table_creator.view(db.session.query(
        Transactions.id,
        Transactions.blockNumber,
        Transactions.timeStamp,
        Transactions.hash,
        Transactions.nonce,
        Transactions.blockHash,
        Transactions.transactionIndex,
        Transactions.trans_from,
        Transactions.trans_to,
        Transactions.value,
        Transactions.gas,
        Transactions.gasPrice,
        Transactions.isError,
        Transactions.contractAddress).all())
    table = table_creator.create(page_num)
    
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
