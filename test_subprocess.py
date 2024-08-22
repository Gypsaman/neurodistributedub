import subprocess
import os
import shutil

def run_forge_homework(repo):

    base_path = './graders/currsubmission'
    subprocess.run(['git', 'clone',repo, os.path.join(base_path,'homework')])
    source_dirs = ['src','test','script']
    for source in source_dirs:
        shutil.rmtree(os.path.join(base_path,'assignment',source),ignore_errors=True)
        shutil.copytree(os.path.join(base_path,'homework',source),os.path.join(base_path,'assignment',source))
    cwd = os.getcwd()
    os.chdir('./graders/currsubmission/assignment')
    result = subprocess.run(['forge','test','--match-path','payUB.t.sol'],stdout=subprocess.PIPE)
    os.chdir(cwd)
    shutil.rmtree(os.path.join(base_path,'homework'),ignore_errors=True)

    return result


repo = 'https://github.com/Gypsaman/payUB.git'
result = run_forge_homework(repo)
print(result.stdout.decode('utf-8'))
