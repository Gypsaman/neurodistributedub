from webproject.models import User, Assets, Wallet
from webproject import db, create_app
import json


def save_data(table,destination:str):
    with create_app().app_context():
        records = table.query.all()
        table_dump = []
        for record in records:
            record_dict = record.__dict__
            if '_sa_instance_state' in record_dict:
                del record_dict['_sa_instance_state']
            table_dump.append(record_dict)
        with open(destination, 'w') as f:
            json.dump(table_dump, f)
    
def populate_data(table,source:str):
    with create_app().app_context():
        with open(source, 'r') as f:
            table_dump = json.load(f)
        for record in table_dump:
            record = table(**record)
            db.session.add(record)
        db.session.commit()

def save_all_data(destination:str=""):
    save_data(User,destination + 'users.json')
    save_data(Assets,destination + 'assets.json')
    save_data(Wallet,destination + 'wallets.json')
    
if __name__ == '__main__':

    
    
