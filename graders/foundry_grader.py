import subprocess
import os
import json
from graders.github import setup_repo, cleanup_repo
import shutil


def compile_project():
    cwd = os.getcwd()
    os.chdir('./graders/currsubmission/foundry')
    result = subprocess.run(['forge','build'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    os.chdir(cwd)
    output = result.stderr if result.returncode  else result.stdout
    return {'return_code':result.returncode,'result':output.decode('utf-8')}

def run_forge(command,source,run_options=None):
    
    cwd = os.getcwd()
    os.chdir('./graders/currsubmission/foundry')
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
    for component,content in components.items():
        if component == 'MasterTest':
            continue
        with open(os.path.join(base_path,'foundry','out',component,f"{content['contract_name']}.json"),'r') as f:
            contract_json = json.load(f)
        abi = contract_json['abi']
        msg += check_abi(abi,content)

    return msg

def foundry_grader(repo,components):
    grade, msg = 0, ''
    destination = 'homework'

    base_path = './graders/currsubmission'
    if not repo:
        return 0, "No Repository Provided"
    
    cleanup_repo(base_path,destination)
    setup_repo(base_path,repo,destination)

    if 'MasterTest' in components:
        content = components['MasterTest']
        shutil.copy(f'./graders/foundry_tests/{content['file']}',f'./graders/currsubmission/foundry/test/{content["file"]}')

    results = {}

    results['compile'] = compile_project()
    
    if results['compile']['return_code'] != 0:
        return results
    
    results['components'] = check_components(base_path,components)


    for component,content in components.items():
        if content['run']['execute']:
            
            results[component] = run_forge(content['run']['type'],content['run']['source'],content['run']['run_options'])
    
    
    cleanup_repo(base_path,destination)

    return results



