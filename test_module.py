from webproject import db, create_app
from webproject.models import User, Wallet,Assignments, Grades
from werkzeug.security import generate_password_hash
from graders.check_submissions import check_submissions
from webproject.models import Submissions
import requests
# import pandas as pd

def create_user():
    with create_app().app_context():
        user = User(first_name='John', last_name='Doe',student_id='99999',section=1,email='cegarcia@bridgeport.edu', password=generate_password_hash('123456', method='sha256'),role='student')
        db.session.add(user)
        db.session.commit()
    
def list_users():
    with create_app().app_context():
        users = User.query.all()
        for user in users:
            print(user.id, user.email, user.student_id)

def remove_wallet():
    with create_app().app_context():
        user = User.query.filter_by(email='cegarcia@bridgeport.edu').first()
        wallet = Wallet.query.filter_by(user_id=user.id).first()
        db.session.delete(wallet)
        db.session.commit()
def check_abi():
    import json
    with create_app().app_context():
        submission = Submissions.query.filter_by(id=449).first()   
        contract = 0xC332E48F97241795dEA9C0DDbF8637E2565A1b18
        abi = [
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "student",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "billAmount",
				"type": "uint256"
			}
		],
		"name": "addBill",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "pay",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [],
		"name": "withdraw",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "billsToPay",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "ethAmount",
				"type": "uint256"
			}
		],
		"name": "getConversionRate",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getPrice",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "studentsBilled",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "viewMyBill",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
        submission.submission = json.dumps({'contract': contract, 'abi': abi})
        # submission.grade = 100
        db.session.commit()
        
def update_section():
    with create_app().app_context():
        user = User.query.filter_by(id=1).first()
        user.section = 1
        db.session.commit()
        
def cross_tab(qry, row_fields,column_field, aggfunc):
    
    cross_qry = 'select' + [f'{field}, ' for field in row_fields] + [f'{aggfunc}({column_field}) as {column_field}'] + 'from' + qry + 'group by' + [f'{field}' for field in row_fields]
    
	
def grades_crosstab():
    import json
    response = requests.get('http://127.0.0.1:5000/gradehistory')
    gradehistory = json.loads(response.content)
    print(gradehistory[0])
    
        
          
grades_crosstab()