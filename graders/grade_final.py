from zipfile import ZipFile
import subprocess
import os
import shutil
import re
import json
import yaml

EXISTING_DIRS = ['payUB-Oracle','submissions']

def get_tree(start_dir):
    dirs = []
    for file in os.listdir(start_dir):
        if file == '_MACOSX':
            continue
        curr_path = os.path.join(start_dir,file)
        if os.path.isdir(curr_path):
            dirs.append(curr_path)
            paths = get_tree(curr_path)
            for p in paths:
                dirs.append(p)
    return dirs

def project_folder():
    
    for file in os.listdir():
        if os.path.isdir(file):
            paths = get_tree(os.path.join(os.getcwd(),file))
            for dir in paths:
                if dir.endswith('scripts'):
                    path = dir
                    break
            else:
                path = ''
            break
    else:
        path = ''
    return path[:-7]

def clean_prior_deployments():
    if os.path.exists('./build/deployments/1337'):
        shutil.rmtree('./build/deployments/1337')
    if os.path.exists('./build/contracts/dependencies/OpenZeppelin'):
        shutil.rmtree('./build/contracts/dependencies/OpenZeppelin')
    for file in os.listdir('./build/contracts'):
        if file.endswith('json'):
            os.remove(os.path.join('./build/contracts',file))

def fix_deployment_versions():
    with open('./brownie-config.yaml','r') as f:
        config = f.read()
    config = config.replace('4.8.0','3.4.0')
    with open('./brownie-config.yaml','w') as f:
        f.write(config)
        
    contractDir = './contracts'
    for file in os.listdir(contractDir):
        with open(os.path.join(contractDir,file),'r') as f:
            script = f.read()
        script = re.sub('pragma solidity .*','pragma solidity 0.7.0;',script)
        with open(os.path.join(contractDir,file),'w') as f:
            f.write(script)
            
    with open('./brownie-config.yaml','r') as f:
        config = yaml.safe_load(f)
    if 'ganache-local' not in config['networks']:
        config['networks']['ganache-local'] = {'verify':False}
    with open('./brownie-config.yaml','w') as f:
        yaml.dump(config,f)
    
        
        
        
def setUp(zipf):
    # clean previous inputs and extract zip file.
    currSubmissionDir = './currsubmission'
    if os.path.exists(currSubmissionDir) == False:
        os.mkdir(currSubmissionDir)
    os.chdir(currSubmissionDir)
    try:
        with ZipFile(zipf,'r') as zipObj:
            zipObj.extractall()
    except:
        return False
    path = project_folder()
    if path != '':
        os.chdir(path)
    clean_prior_deployments()
    fix_deployment_versions()
    if os.path.exists('.env') == False:
        with open('.env','w') as f:
            f.write('WEB3_INFURA_PROJECT_ID=0')
    return True

def cleanUp(orig_dir,delete=True):
    os.chdir(orig_dir)
    if delete:
        for file in os.listdir(orig_dir):
            curr_file = os.path.join(orig_dir,file)
            if os.path.isdir(curr_file) and file not in EXISTING_DIRS:
                shutil.rmtree(curr_file)


def gradeFinal():

    # Check that there is at least one script and utilize the first one.
    
    scripts = ['deploy_token.py','deploy_nft.py','transfer_token_nft.py','check_nft_balance.py','nft_mint.py']
    
    grade = 0
    
    for script in scripts:

        # Run the brownie script
        result = subprocess.run(['brownie', 'run', script, '--network', 'ganache-local'],stdout=subprocess.PIPE)
        

        brownieOutput = result.stdout.decode('utf-8')


        # Analyze output of brownie
        contract = ''

        invalidSyntax = re.search(r'invalid syntax',brownieOutput)
        if invalidSyntax:
            continue

        isError = re.search(r'[Ee]rror',brownieOutput)
        if isError:
            continue
        

        if script.startswith('deploy'):
            matches = re.findall(r'deployed at: 0x[a-zA-Z0-9]{40}',brownieOutput)
            if matches:
                grade += 20
            continue
        if script == 'transfer_token_nft.py':
            matches = re.findall(r'transfer confirmed',brownieOutput)
            if matches:
                grade += 20
            continue
        if script == 'check_nft_balance.py':
            matches = re.findall(r'1000000000000000000000',brownieOutput)
            if matches:
                grade += 20
                continue
            matches = re.findall(r'1000',brownieOutput)
            if matches:
                grade += 20
            continue
        if script == 'nft_mint.py':
            matches = re.findall(r'createLogoNFT confirmed',brownieOutput)
            if matches:
                grade += 20
                continue
            matches = re.findall(r'createLogoNft confirmed',brownieOutput)
            if matches:
                grade += 20
                continue
            matches = re.findall(r'CreateLogoNFT confirmed',brownieOutput)
            if matches:
                grade += 20
            continue
    return grade
            

def SubmissionInfo(submission):
    data = submission.split('_')
    student = data[0]
    id = data[1] if data[1] != 'LATE' else data[2]

    return student, id

def save_results(results):
    
    with open(resultFile,'w') as f:
        json.dump(results,f)

    return

def export_grades():
    with open('results.json','r') as f:
        results = json.load(f)

    with open('grades.csv','w') as grades:
        for id,info in results.items():
            grades.write(f'{id},{info["student"]},{info["grade"]}\n')



if __name__ == '__main__':

    # export_grades()
    # exit()
    resultFile = 'results.json'
    if os.path.exists(resultFile):
        with open(resultFile,'r') as f:
            results = json.load(f)
    else: 
        results = {}

    curr_dir = os.getcwd()
    submissionPath = os.path.join(curr_dir,'submissions')
    for file in [f for f in os.listdir('.\submissions') if f.endswith('zip')]:
        student, id = SubmissionInfo(file)
        if id in results and results[id]['grade'] in [0,100]:
            continue
        print(f'Processing {id}-{student}....')
        if setUp(os.path.join(submissionPath,file)):
            grade = gradeFinal()
        else:
            grade = 0

        results[id] = {"student":student,"grade":grade}
        print(results[id])

        cleanUp(curr_dir,delete=True)
        
        

    save_results(results)
    export_grades()
        