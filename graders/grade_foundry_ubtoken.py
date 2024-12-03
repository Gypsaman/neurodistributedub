from graders.foundry_grader import foundry_grader
import os
from web3 import Web3
from webproject.modules.dotenv_util import initialize_dotenv
initialize_dotenv()

PROVIDER = os.getenv('ANVIL_PROVIDER')
PRIVATE_KEY = os.getenv('ANVIL_PRIVATE_KEY')


homework_components = {
    'UBToken.sol': {
        'contract_name': 'UBToken',
        'constructor': ['string','string','uint256'],
        'functions': ['transfer','balanceOf'],
        'run':{'execute':False,'type':'','source':'','run_options': []},

    },
    'UBToken.s.sol': {
        'contract_name': 'UBTokenDeploy',
        'constructor': [],
        'functions': ['run'],
        'run':{'execute':True,
                'type':'script',
                'source':'script/UBToken.s.sol',
                'run_options': [f'--rpc-url',f'{PROVIDER}',f'--private-key',f'{PRIVATE_KEY}','--broadcast']
                },
    }
}   
def grade_foundry_UBToken(repo):

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
        grade += 20
         
    book_s_broadcast = results['UBToken.s.sol']['broadcast']
    account = 0x9965507D1a55bcC2695C58ba16FB37d819B0A4dc
    for tx in book_s_broadcast['transactions']:
        if tx['transactionType'] == "CREATE" and tx['contractName'] == 'UBToken':
            contract =  tx['contractAddress']
            result = get_balance(contract,results['abi']['UBToken.sol'],account)
            if result == 100 * 10**18:
                grade += 25
            else:
                msg += f'Account {account} did not get 100 Tokens \n'
            break
    else:
        msg += 'UBToken Contract Not Deployed in Script\n'

    if grade == 100:
        msg = 'Great Job on Assignment'
        
    return grade,msg


def get_balance(contract,abi,account):
    w3 = Web3(Web3.HTTPProvider(PROVIDER))
    contract = w3.eth.contract(address=Web3.to_checksum_address(contract),abi=abi)
    return contract.functions.balanceOf("0x9965507D1a55bcC2695C58ba16FB37d819B0A4dc").call()