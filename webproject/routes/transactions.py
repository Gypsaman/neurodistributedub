from flask import Blueprint,render_template,request
from flask_login import current_user
from webproject.models import User,Wallet,Transactions
from webproject.modules.web3_interface import  getEthTrans
from webproject.modules.table_creator import TableCreator,Field,timestamp_to_date,short_hash,wei_to_eth,true_false,yes_no
from webproject import db

from flask_login import login_required


trans = Blueprint('trans',__name__)

@trans.route('/transactions/<int:page_num>')
@login_required
def transactions(page_num):
    fields = {
            'id': Field(None,None),
            'blockNumber': Field(None, 'Block Number'),
            'timeStamp': Field(timestamp_to_date, 'Date'),
            'hash': Field(short_hash, 'Hash'),
            'nonce': Field(None, 'Nonce'),
            'blockHash': Field(short_hash, 'Block Hash'),
            'transactionIndex':Field(None, 'Transaction Index'),
            'trans_from': Field(short_hash, 'From'),
            'trans_to': Field(short_hash, 'To'),
            'value': Field(wei_to_eth, 'Value'),
            'gas': Field(wei_to_eth, 'Gas'),
            'gasPrice': Field(wei_to_eth, 'Gas Price'),
            'isError': Field(yes_no, 'Is Error'),
            'contractAddress': Field(short_hash, 'Contract Address')
    }
    table_creator = TableCreator('Transactions',fields,condition=f'user_id={current_user.id}',actions=['View'])
    table_creator.set_items_per_page(15)

    table_creator.create_view()
    table = table_creator.create(page_num)
    
    return render_template('trans/transactions.html',table=table)

@trans.route('/transactions/view/<int:page_num>/<int:tran_id>')
@login_required
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
