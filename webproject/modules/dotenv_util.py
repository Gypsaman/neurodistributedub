import os
from dotenv import load_dotenv

def initialize_dotenv():
    # pass
    
    load_dotenv(os.path.join(get_cwd(),".env"))
    
def get_cwd():
    cwd = os.getcwd()
    cwd = '/var/www/dna' if cwd == '/' else cwd
    # cwd = os.path.join(cwd,'neurodistributedub') if cwd.endswith('neurodistributed') else cwd
    return cwd