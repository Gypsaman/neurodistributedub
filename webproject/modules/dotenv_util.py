import os
from dotenv import load_dotenv

def initialize_dotenv():
    cwd = os.getcwd()
    cwd = os.path.join(cwd,'neurodistributedub') if cwd.endswith('neurodistributed') else cwd
    load_dotenv(os.path.join(cwd,".env"))