from webproject.modules.web3_interface import get_eth_balance
from web3 import Web3,HTTPProvider
import json
import shutil
import os

UPLOADPATH = os.getenv("UPLOADPATH")
STOREPATH = os.getenv("STOREPATH")
myaccount = os.getenv("MYWALLET")


def get_contract(contractAddress,abiFile):

    w3 = Web3(HTTPProvider('https://goerli.infura.io/v3/a6285c05a4094c4ea4a16c1395c44881'))
    with open(abiFile,'r') as f:
        abi = json.load(f)
    try:
        contract = w3.eth.contract(address=w3.toChecksumAddress(contractAddress),abi=abi)
    except:
        contract = None
    
    return contract
def rentCar_Grader(contractAddress):

    rentCar = get_contract(contractAddress,'rentCar_ABI.json')

    if rentCar is None:
        return 0

    try:
        _,_,_,_,rentAmt = rentCar.functions.carDetails().call({"from":myaccount})
    except:
        rentAmt = 0
    
    try:
        tx = rentCar.functions.rentCar().call({'from':myaccount,'value':rentAmt})
        rentOk = True
    except:
        rentOk = False

    grade = 75
    if rentAmt  > 0 and rentOk:
        grade = 100
    elif rentAmt > 0:
        grade = 90

    return grade

def MidTerm_Grader(contractAddress):

    midTerm = get_contract(contractAddress,'MidTerm_ABI.json')

    if midTerm is None:
        return 0

    try:
        value = midTerm.functions.getValue().call({"from":myaccount})
    except:
        value = 0

    grade = 75
    if value==100:
        grade = 100
    elif value > 0:
        grade = 80
    
    
    return grade

def MyID_Grader(contractAddress):

    myID = get_contract(contractAddress,'myID_ABI.json')

    if myID is None:
        return 0

    try:
        id = myID.functions.getID().call({"from":myaccount})
    except:
        id = ""

    grade = 75
    if isinstance(id,tuple):
        grade = 100
    
    
    return grade

def payUB_Grader(contractAddress):

    payUB = get_contract(contractAddress,'payUB_ABI.json')

    if payUB is None:
        return 0

    try:
        billtopay = payUB.functions.billsToPay(myaccount).call()
    except:
        billtopay = -1
    try:
        mybill = payUB.functions.viewBill().call({"from":Web3.toChecksumAddress(myaccount)})
    except:
        try:
            mybill = payUB.functions.viewMyBill().call({"from":Web3.toChecksumAddress(myaccount)})
        except:
            mybill = -1
    
    grade = 75
    if billtopay == 500:
        grade = 85
    if mybill == 500:
        grade = 100
    
    return grade

def sha256_grader(submission:str) -> None:
    cwd = os.getcwd()
    cwd = os.path.join(cwd,'neurodistributedub') if cwd == '\home\neurodistributed' else cwd
    shutil.copy(submission,os.path.join(cwd,'SHAIMPORT.py'))
    from SHAIMPORT import SHA256
    correcthash = "d6e8f9655184c6f96b24dc3df0c8eb88678181c79f4d7f809b51e88288976f7d"
    try:
        hash = SHA256('Cesar Garcia')
    except:
        hash = "" 
    if isinstance(hash,list):
        hash = ''.join(hash)
    if hash == correcthash:
        return 100
    if len(hash) == len(correcthash):
        return 90

    return 80

graders= {
    "SHA256": sha256_grader,
    # "ECC": ecc_grader,
    # "Wallet": wallet_grader,
}
def call_grader(assignment:str,submission:str) -> int:
   
   return graders[assignment](submission)
    
    