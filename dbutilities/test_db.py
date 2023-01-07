from webproject.models import User, Wallet, Assets, Transactions, Assignments,Submissions
from webproject import create_app, db
from webproject.modules.table_creator import table_creator
from datetime import datetime as dt

def print_data():
    with create_app().app_context():
        
        print('list of users...')
        users = User.query.all()
        if len(users) == 0:
            print("\tNo users found")
        for user in users:
            print(f'\t{user}')
        
        print('list of wallets...')
        wallets = Wallet.query.all()
        if len(wallets) == 0:
            print("\tNo wallets found")
        for wallet in wallets:
            print(f'\t{wallet}')
            
        print('list of transactions...')
        transactions = Transactions.query.all()
        if len(transactions) == 0:
            print("\tNo transactions found")
        for transaction in transactions:
            print(f'\t{transaction}')
            
        print('list of assets...')
        assets = Assets.query.all()
        if len(assets) == 0:
            print("\tNo assets found")
        for asset in assets:
            print(f'\t{asset}')
            
        print('list of assignments...')
        assignments = Assignments.query.all()
        if len(assignments) == 0:
            print("\tNo assignments found")
        for assignment in assignments:
            print(f'\t{assignment}')
            
        print('list of submissions...')
        submissions = Submissions.query.all()
        if len(submissions) == 0:
            print("\tNo submissions found")
        for submission in submissions:
            print(f'\t{submission}')
            
            
def update_timestamp():
    with create_app().app_context():
        assets = Assets.query.all()
        for asset in assets:
            asset.timestamp = dt.now()
            db.session.commit()
            
def delete_rows(table):
    with create_app().app_context():
        rows = table.query.all()
        for row in rows:
            db.session.delete(row)
            db.session.commit()
            
def get_column(table,column):
    with create_app().app_context():
        rows = table.query.all()
        col = []
        for row in rows:
            col.append(getattr(row,column))
            break
        return col
def test_table_creator():
    with create_app().app_context():
        table,pages = table_creator('Transactions',Transactions.query.all(),30,1)
    return table,pages
    
def temp_update_asset_type():
    with create_app().app_context():
        assets = Assets.query.all()
        for asset in assets:
            if asset.asset_type == 2:
                asset.asset_type = 1
            elif asset.asset_type == 1:
                asset.asset_type = 2
                    
            db.session.commit()
if __name__ == '__main__':

    print_data()
