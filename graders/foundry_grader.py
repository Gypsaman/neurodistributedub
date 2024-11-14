import subprocess
import os
import json
from graders.github import setup_repo, cleanup_repo
import shutil
from web3 import Web3


def compile_project():
    cwd = os.getcwd()
    os.chdir('/var/www/dna/graders/currsubmission/foundry')
    result = subprocess.run(['forge','build'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    os.chdir(cwd)
    output = result.stderr if result.returncode  else result.stdout
    return {'return_code':result.returncode,'result':output.decode('utf-8')}

def run_forge(command,source,run_options=None):
    
    cwd = os.getcwd()
    os.chdir('/var/www/dna/graders/currsubmission/foundry')
    forge_process = ['forge',command,source] 
    if run_options:
        forge_process += run_options
    result = subprocess.run(forge_process,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    os.chdir(cwd)
    output = result.stdout + result.stderr
    return {'return_code':result.returncode,'result':output.decode('utf-8')}

def check_abi(abi,content):
    msg = ''
    # Check for Constructor
    if content['constructor']:
        if not [entry for entry in abi if entry['type']=='constructor']:
            msg += 'Constructor Not Found\n'

    # Check for Functions
    for function in content['functions']:
        if not [x for x in abi if x['type']=='function' and x['name'] == function]:
            msg += f'"{function}" Not Found\n'

    return msg

def check_components(base_path,components):
    msg = ''
    ABIs = {}
    for component,content in components.items():
        if component == 'MasterTest':
            continue
        try:
            with open(os.path.join(base_path,'foundry','out',component,f"{content['contract_name']}.json"),'r') as f:
                contract_json = json.load(f)
            abi = contract_json['abi']
            ABIs[component] = abi
            msg += check_abi(abi,content)
        except Exception as e:
            msg += f'Error {component} - {e}\n'

    return  msg,ABIs

def foundry_grader(repo,components):
    grade, msg = 0, ''
    destination = 'homework'

    base_path = '/var/www/dna/graders/currsubmission'
    if not repo:
        return 0, "No Repository Provided"
    
    cleanup_repo(base_path,destination)
    setup_repo(base_path,repo,destination)

    if 'MasterTest' in components:
        content = components['MasterTest']
        shutil.copy(f'/var/www/dna/graders/foundry_tests/{content['file']}',f'/var/www/dna/graders/currsubmission/foundry/test/{content["file"]}')

    results = {}

    results['compile'] = compile_project()
    
    if results['compile']['return_code'] != 0:
        return results
    
    results['components'],results['abi'] = check_components(base_path,components)
    for component,content in components.items():
        if content['run']['execute']:
            results[component] = run_forge(content['run']['type'],content['run']['source'],content['run']['run_options'])
            results[component]['broadcast'] = get_broadcast(component,base_path)

    cleanup_repo(base_path,destination)

    return results

def contract_from_last_tx(abi):
    contract = None
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
    latest_block = w3.eth.get_block('latest')
    if not latest_block['transactions']:
        return None
    last_tx_hash = latest_block['transactions'][-1]
    tx = w3.eth.get_transaction(last_tx_hash)
    if tx['to']:
        return None
    tx_receipt = w3.eth.get_transaction_receipt(last_tx_hash)
    contract_address = tx_receipt['contractAddress']
    contract = w3.eth.contract(address=contract_address,abi=abi)
    return contract

def get_broadcast(component,base_path):
    try:
        broadcast = json.load(open(os.path.join(base_path,'foundry','broadcast',component,'31337','run-latest.json')))
    except:
        broadcast = None
    return broadcast