from graders.foundry_grader import foundry_grader
import os

PROVIDER = os.getenv('LOCAL_PROVIDER')
PRIVATE_KEY = os.getenv('ANVIL_PRIVATE_KEY')


homework_components = {
    'Books.sol': {
        'contract_name': 'Books',
        'constructor': ['string','string','uint256'],
        'functions': ['update_pages','get_book'],
        'run':{'execute':False,'type':'','source':'','run_options': []}
    },
    'Books.s.sol': {
        'contract_name': 'DeployBooks',
        'constructor': [],
        'functions': ['run'],
        'run':{'execute':True,
                'type':'script',
                'source':'script/Books.s.sol',
                'run_options': [f'--rpc-url',f'{PROVIDER}',f'--private-key',f'{PRIVATE_KEY}','--broadcast']
                }
    },
    'Books.t.sol': {
        'contract_name': 'TestBooks',
        'constructor': [],
        'functions': ['setUp','test_update_pages','test_get_book'],
        'run':{'execute':True,'type':'test','source':'-vv','run_options': ['--nmt','Master']}
    },
    'MasterTest': {
        'file': 'Books_Master.t.sol',
        'run':{'execute':True,'type':'test','source':'-vv','run_options': ['--mt', 'Master']}
    }
}   
def grade_foundry(repo):
    grade,msg = 0,''

    results = foundry_grader(repo, homework_components)

    if results['compile']['return_code'] != 0:
        return grade,results['compile']['result']
    grade += 25

    if results['components']:
        return grade,results['components']
    grade += 30

    for component,content in homework_components.items():
        if content['run']['execute'] == False:
            continue
        if results[component]['return_code'] != 0:
            return grade,f'\n{component} FAILED\n\n{results[component]['result']}'
        grade += 15
         
    if grade == 100:
        msg = 'Great Job on Assignment'
        
    return grade,msg