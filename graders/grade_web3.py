import subprocess
import os
import shutil
import re
from web3 import Web3
import stat
import sys

def setup_repo(base_path,repo):

    result = subprocess.run(['git', 'clone',repo, os.path.join(base_path,'python')],stdout=subprocess.PIPE)
    if result.returncode != 0:
        raise Exception("Could not clone Repository")
    if os.path.exists(os.path.join(base_path,'python','venv')):
        shutil.rmtree(os.path.join(base_path,'python','venv'),onerror=on_rm_error)


def on_rm_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)  # Change the permission to writable
    func(path) 
def cleanup_repo(base_path):
    if os.path.exists(os.path.join(base_path,'python')):
        shutil.rmtree(os.path.join(base_path,'python'),onerror=on_rm_error)

def run_test(python_file):
    
    cwd = os.getcwd()
    os.chdir('./graders/currsubmission/python')
    if not os.path.exists(python_file):
        return f"Error:{python_file} not found"
    # result = subprocess.run(['python',python_file],stdout=subprocess.PIPE)
    try:
        result = subprocess.run([sys.executable, python_file], stdout=subprocess.PIPE)
    except Exception as e:
        os.chdir(cwd)
        return e
    os.chdir(cwd)
    return result.stdout.decode('utf-8')

def check_components(base_path,program_file):
    grade, msg = 0, ''
    base_path = os.path.join(base_path,'python')
    if not os.path.exists(os.path.join(base_path,program_file)):
        msg =  f"Error: {program_file} not found"
    else:
        grade += 10
    if os.path.exists(os.path.join(base_path,'.env')):
        msg = f".env included in Repository.  Your funds will be stolen."
    else:
        grade += 10
    with open(os.path.join(base_path,program_file),'r') as f:
        content = f.read()
        for component in ['ANVIL_ACCOUNT','ANVIL_PRIVATE_KEY','LOCAL_PROVIDER']:
            if component not in content:
                msg += f"{component} not found in {program_file}\n"
            else:
                grade += 10
        

    return grade, msg

def grade_web3(repo,program_file):

    provider = os.getenv("LOCAL_PROVIDER")
    connection = Web3(Web3.HTTPProvider(provider))

    base_path = './graders/currsubmission'
    cleanup_repo(base_path)
    grade, msg = 0, ''

       
    try:
        setup_repo(base_path,repo)
    
    except Exception as e:
        grade,msg = 0, f"Could not retrieve Repository from {repo}.\n  {e}"
        return grade,msg
    
    grade, msg = check_components(base_path,program_file)
    
    result = run_test(program_file)
    if 'Error' in result or result =="":
        msg = 'Error in running Assignment\n' + result
        return grade, msg
    
    grade += 20

    p = re.compile('0x[a-zA-Z0-9]{40}')

    regex = p.search(result)
    if regex:
        contract_address = regex.group()
        grade += 10
        value = connection.eth.get_storage_at(contract_address,0)
        if int.from_bytes(value) == 5341:
            grade += 20

    else:
        msg = "Error: Contract Address not found in output\n" + result
    cleanup_repo(base_path)
    return grade, msg if msg > '' else 'Assignment is correct'


if __name__ == '__main__':
    
    grade, msg = grade_web3('https://github.com/Gypsaman/web3-tutorial.git','./src/Interact.py')
    print(grade,msg)