from webproject import create_app, db
from webproject.models import Assignments,Submissions,Grades, User,Assets
from webproject.modules.table_creator import TableCreator, Field,timestamp_to_date,short_hash,wei_to_eth,asset_type_string,yes_no


with create_app().app_context():
    
    # qry = db.session.execute("Select assignments.name, grade from Grades join Assignments on Grades.assignment = Assignments.id ")
#     qry = db.session.execute('Select t2.name,t1.grade from Grades as t1 join Assignments as t2 on t1.assignment = t2.id ')
    # 'Select assignment.name,grade,dategraded from Grades join Assignments on Grades.assignment = Assignments.id '
#     for row in qry:
#         print(row)
        
    
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
    table_creator = TableCreator('Transactions',fields,actions=['View'])
    table_creator.set_items_per_page(15)

    table_creator.create_view()
    table = table_creator.create(1)