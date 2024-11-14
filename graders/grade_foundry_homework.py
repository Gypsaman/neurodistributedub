from graders.foundry_grader import foundry_grader
import os
from web3 import Web3

PROVIDER = os.getenv('LOCAL_PROVIDER')
PRIVATE_KEY = os.getenv('ANVIL_PRIVATE_KEY')


homework_components = {
    'Books.sol': {
        'contract_name': 'Books',
        'constructor': ['string','string','uint256'],
        'functions': ['update_pages','get_book'],
        'run':{'execute':False,'type':'','source':'','run_options': []},

    },
    'Books.s.sol': {
        'contract_name': 'DeployBooks',
        'constructor': [],
        'functions': ['run'],
        'run':{'execute':True,
                'type':'script',
                'source':'script/Books.s.sol',
                'run_options': [f'--rpc-url',f'{PROVIDER}',f'--private-key',f'{PRIVATE_KEY}','--broadcast']
                },
    },
    'Books.t.sol': {
        'contract_name': 'TestBooks',
        'constructor': [],
        'functions': ['setUp','test_update_pages','test_get_book'],
        'run':{'execute':True,'type':'test','source':'-vv','run_options': ['--nmt','Master']},
    },
    'MasterTest': {
        'file': 'Books_Master.t.sol',
        'run':{'execute':True,'type':'test','source':'-vv','run_options': ['--mt', 'Master']},

    }
}   
def grade_foundry_homework(repo):

    grade,msg = 0,''

    results = foundry_grader(repo, homework_components)

    if results['compile']['return_code'] != 0:
        return grade,results['compile']['result']
    msg += 'Compiled Successfully'
    grade += 25

    if results['components']:
        return grade,results['components']
    msg += '\nAll Components Found'
    grade += 30

    for component,content in homework_components.items():
        if content['run']['execute'] == False:
            continue
        if results[component]['return_code'] != 0:
            msg += f'\n{component} FAILED\n\n{results[component]['result']}'
            continue
        grade += 10
         
    # book_s_broadcast = results['Books.s.sol']['broadcast']
    # for tx in book_s_broadcast['transactions']:
    #     if tx['transactionType'] == "CREATE" and tx['contractName'] == 'Books':
    #         contract =  tx['contractAddress']
    #         result = get_book(contract,results['abi']['Books.sol'])
    #         if result[0] == 'Programming Foundry' and result[2] == 100:
    #             grade += 15
    #         else:
    #             msg += 'get_book did not return correct values\n'
    #         break
    # else:
    #     msg += 'Books Contract Not Deployed in Script\n'

    if grade == 100:
        msg = 'Great Job on Assignment'
        
    return grade,msg


def get_book(contract,abi):
    w3 = Web3(Web3.HTTPProvider(PROVIDER))
    contract = w3.eth.contract(address=Web3.to_checksum_address(contract),abi=abi)
    return contract.functions.get_book().call()