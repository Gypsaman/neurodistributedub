import subprocess
import os
import shutil

def setup_repo(base_path,repo):


    subprocess.run(['git', 'clone',repo, os.path.join(base_path,'homework')])
    source_dirs = ['src','test','script']
    for source in source_dirs:
        shutil.rmtree(os.path.join(base_path,'foundry',source),ignore_errors=True)
        shutil.copytree(os.path.join(base_path,'homework',source),os.path.join(base_path,'foundry',source))
    
def cleanup_repo(base_path):

    shutil.rmtree(os.path.join(base_path,'homework'),ignore_errors=True)

def run_forge_test():
    
    
    cwd = os.getcwd()
    os.chdir('./graders/currsubmission/foundry')
    result = subprocess.run(['forge','test','--match-path','payUB.t.sol'],stdout=subprocess.PIPE)
    os.chdir(cwd)
    return result


def grade_foundry(repo):
    base_path = './graders/currsubmission'
    repo = repo if repo else 'https://github.com/Gypsaman/payUB.git'
    
    setup_repo(base_path,repo)
    result = run_forge_test()
    cleanup_repo(base_path)

    print(result.stdout.decode('utf-8'))