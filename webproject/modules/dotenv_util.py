import os
from dotenv import load_dotenv

def initialize_dotenv():
    
    load_dotenv(os.path.join('\var\www\neurodistributedub',".env"))
    
def get_cwd():
    cwd = os.getcwd()
    # cwd = os.path.join(cwd,'neurodistributedub') if cwd.endswith('neurodistributed') else cwd
    return cwd