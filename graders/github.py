from webproject.models import Submissions
import os
import shutil
import stat
import subprocess

def check_duplicate_repo(assignment,repo,user_id):
    # Check if repo already exists
    existing_repo = Submissions.query.filter(
        Submissions.assignment == assignment, 
        Submissions.submission == repo,
        Submissions.user_id != user_id).first()
    if existing_repo:
        return True
    return False

def setup_repo(base_path,repo,destination):


    result = subprocess.run(['git', 'clone',repo, os.path.join(base_path,destination)])
    if result.returncode != 0:
        return False
    source_dirs = ['src','test','script']
    for source in source_dirs:
        shutil.rmtree(os.path.join(base_path,'foundry',source),ignore_errors=True)
        if os.path.exists(os.path.join(base_path,destination,source)):
            shutil.copytree(os.path.join(base_path,destination,source),os.path.join(base_path,'foundry',source))
    shutil.rmtree(os.path.join(base_path,'foundry','out'),ignore_errors=True)
    shutil.rmtree(os.path.join(base_path,'foundry','cache'),ignore_errors=True)
    shutil.rmtree(os.path.join(base_path,'foundry','broadcast'),ignore_errors=True)

    return True

def on_rm_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)  # Change the permission to writable
    func(path) 

def cleanup_repo(base_path,destination):
    if os.path.exists(os.path.join(base_path,destination)):
        shutil.rmtree(os.path.join(base_path,destination),onerror=on_rm_error)

