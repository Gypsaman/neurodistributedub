from zipfile import ZipFile
from webproject.modules.dotenv_util import get_cwd
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

def currSubmissionsPath():
    cwd = get_cwd()
    currSubmissionDir = os.path.join(cwd,'graders','currsubmission')
    return currSubmissionDir


def project_folder():
    currSubmissionDir = currSubmissionsPath()
    if 'scripts' in os.listdir(currSubmissionDir):
        return currSubmissionDir
    for file in os.listdir(currSubmissionDir):
        if 'MACOSX' in file:
            continue
        if os.path.isdir(os.path.join(currSubmissionDir,file)):
            paths = get_tree(os.path.join(currSubmissionDir,file))
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

def clean_prior_deployments(path):
    if os.path.exists(os.path.join(path,'build/deployments/1337')):
        shutil.rmtree(os.path.join(path,'build/deployments/1337'))
    if os.path.exists(os.path.join(path,'build/contracts/dependencies/OpenZeppelin')):
        shutil.rmtree(os.path.join(path,'build/contracts/dependencies/OpenZeppelin'))
    for file in os.listdir(os.path.join(path,'build/contracts')):
        if file.endswith('json'):
            os.remove(os.path.join(path,'build/contracts',file))

def fix_deployment_versions(path):
    with open(os.path.join(path,'brownie-config.yaml'),'r') as f:
        config = f.read()
    config = config.replace('4.8.0','3.4.0')
    with open(os.path.join(path,'brownie-config.yaml'),'w') as f:
        f.write(config)
        
    contractDir = os.path.join(path,'contracts')
    for file in os.listdir(contractDir):
        with open(os.path.join(contractDir,file),'r') as f:
            script = f.read()
        script = re.sub('pragma solidity .*','pragma solidity 0.7.0;',script)
        with open(os.path.join(contractDir,file),'w') as f:
            f.write(script)
            
    # with open(os.path.join(currSubmissionsPath(),'./brownie-config.yaml'),'r') as f:
    #     config = yaml.safe_load(f)
    # if 'ganache-local' not in config['networks']:
    #     config['networks']['ganache-local'] = {'verify':False}
    # with open('./brownie-config.yaml','w') as f:
    #     yaml.dump(config,f)
    
        
        
        
def setUp(zipf):
    # clean previous inputs and extract zip file.
    currSubmissionDir = currSubmissionsPath()
    if os.path.exists(currSubmissionDir):
        cleanUp()
    else:
        os.mkdir(currSubmissionDir)
    
    # import pathlib
    # zipf = pathlib.Path(zipf)
    try:
        with ZipFile(zipf,'r') as zipObj:
            zipObj.extractall('./graders/currsubmission')
    except:
        return False
    
    path = project_folder()
    clean_prior_deployments(path)
    fix_deployment_versions(path)

    return True

def cleanUp():
    cwd = get_cwd()
    currSubmissionDir = os.path.join(cwd,'graders','currsubmission')
    
    for file in os.listdir(currSubmissionDir):
        curr_file = os.path.join(currSubmissionDir,file)
        if os.path.isdir(curr_file):
            shutil.rmtree(curr_file)
        else:
            os.remove(curr_file)


def gradeFinal(submission):
    
    if not submission.endswith('.zip'):
        return 0, 'Submission must be a zip file'
    
    if not setUp(submission):
        return 0, 'invalid submission'

    grade = 0
    
    script = 'finalexam'
    # Run the brownie script
    currSubmissionDir = project_folder()
    cwd = os.getcwd()
    try:
        os.chdir(currSubmissionDir)
        result = subprocess.run(['brownie', 'run', script],stdout=subprocess.PIPE)
    except Exception as e:
        raise Exception(f'Error running brownie\n\n{e}')
    finally:
        os.chdir(cwd)
    brownieOutput = result.stdout.decode('utf-8')


    # Analyze output of brownie

    invalidSyntax = re.search(r'invalid syntax',brownieOutput)
    if invalidSyntax:
        return grade,'invalid syntax'

    isError = re.search(r'[Ee]rror',brownieOutput)
    if isError:
        return grade, 'Error'
    
    grade = 30
    elements = [
        ['UBToken deployed at:','UBToken not Deployed'],
        ['UBToken.transfer confirmed','UBToken.transfer not confirmed'],
        ['UBNFT deployed at:','UBNFT not Deployed'],
        ['UBNFT.registerToken confirmed','UBNFT.registerToken not confirmed'],
        ['UBToken.approve confirmed','UBToken.approve not confirmed'],
        ['UBNFT.depositTokens confirmed','UBNFT.depositTokens not confirmed'],
        ['UBNFT.createLogoNFT','UBNFT.createLogoNFT not confirmed']
    ]
    
    msg = ''
    for element in elements:
        matches = re.findall(element[0],brownieOutput)
        if matches:
            grade += 10
        else:
            msg += element[1] + '\n'
    
    return grade,msg
            

def SubmissionInfo(submission):
    data = submission.split('_')
    student = data[0]
    id = data[1] if data[1] != 'LATE' else data[2]

    return student, id

def save_results(results):
    
    with open(resultFile,'w') as f:
        json.dump(results,f)

    return





    
        
        

        