from webproject.modules.dotenv_util import get_cwd
import os
from zipfile import ZipFile
import shutil
import re
import subprocess

def get_tree(start_dir):
    dirs = []
    for file in os.listdir(start_dir):
        if 'MACOSX' in file:
            continue
        curr_path = os.path.join(start_dir,file)
        if os.path.isdir(curr_path):
            dirs.append(curr_path)
            paths = get_tree(curr_path)
            for p in paths:
                dirs.append(p)
    return dirs


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

def set_up_zipfile(zipf):
    # clean previous inputs and extract zip file.
    currSubmissionDir = currSubmissionsPath()
    if os.path.exists(currSubmissionDir):
        cleanup_zip()
    else:
        os.mkdir(currSubmissionDir)
    
    # import pathlib
    # zipf = pathlib.Path(zipf)
    with ZipFile(zipf,'r') as zipObj:
        zipObj.extractall(currSubmissionDir)
        
    # shutil.copy(os.path.join(cwd,'.env'),currSubmissionDir)
        
def cleanup_zip():
    cwd = get_cwd()
    currSubmissionDir = os.path.join(cwd,'graders','currsubmission')
    
    for file in os.listdir(currSubmissionDir):
        curr_file = os.path.join(currSubmissionDir,file)
        if os.path.isdir(curr_file):
            shutil.rmtree(curr_file)
        else:
            os.remove(curr_file)

def currSubmissionsPath():
    cwd = get_cwd()
    currSubmissionDir = os.path.join(cwd,'graders','currsubmission')
    return currSubmissionDir



def brownie_grader(submission:str) :
      # Check that there is at least one script and utilize the first one.
    if not submission.endswith('.zip'):
        return 0, 'Submission must be a zip file'
    set_up_zipfile(submission)
    
    currSubmissionDir = project_folder()
    scriptsPath = os.path.join(currSubmissionDir,'scripts')
    script = ''
    if 'deploy.py' in os.listdir(scriptsPath):
        script = 'deploy.py'
    else:
        for s in os.listdir(scriptsPath):
            if s.endswith('.py'):
                script = s
                break
            
    if script == '':
        return 0,'No script found' 

    # Run the brownie script
    # result = subprocess.run(['brownie', 'run', script, '--network', 'ganache-local'],stdout=subprocess.PIPE)
    cwd = os.getcwd()
    try:
        os.chdir(currSubmissionDir)
        result = subprocess.run(['brownie', 'run', script],stdout=subprocess.PIPE)
    except Exception as e:
        raise Exception(f'Error running brownie\n\n{e}')
    finally:
        os.chdir(cwd)

    brownieOutput = result.stdout.decode('utf-8')

    brownieOutput = brownieOutput.replace('\x1b','').replace('[0;1;34m','').replace('[0;m','')

    # Analyze output of brownie
    
    isError = re.search(r'[Ee]rror',brownieOutput)
    if isError:
        return 0,isError.group(0)
    
    invalidSyntax = re.search(r'invalid syntax',brownieOutput)
    if invalidSyntax:
        return 70,invalidSyntax.group(0)


    matches = re.findall(r'deployed at: 0x[a-zA-Z0-9]{40}',brownieOutput)
    contract = ''
    for match in matches:
        contract = re.findall(r'0x[a-zA-Z0-9]{40}',match)[0]
    if contract.startswith('0x'):
        return 100,'Valid deployement'
    
    return 70, 'deployment did not generate a contract'


