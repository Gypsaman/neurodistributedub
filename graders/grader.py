from webproject.modules.web3_interface import get_eth_balance, getContractCreator
from web3 import Web3,HTTPProvider
import json
import shutil
import os
import numpy as np
from webproject.modules.dotenv_util import get_cwd
from webproject.models import Wallet

UPLOADPATH = os.getenv("UPLOADPATH")
STOREPATH = os.getenv("STOREPATH")
myaccount = os.getenv("MYWALLET")


def get_dict_from_string(dictstring):
    try:
        dict = json.loads(dictstring)
    except Exception as e:
        dict = {}
        
    return dict

def get_abi_functions(abi):
   
    return [i['name'] for i in abi if i['type'] == 'function']

def has_constructor(abi):
    return 'constructor' in [i['type'] for i in abi]
   
def get_constructor(abi):
    constructor_arr = [i for i in abi if i['type'] == 'constructor']
    constructor = constructor_arr[0] if len(constructor_arr) > 0 else None
    return constructor

def get_contract_info(Address_ABI):
    
    Address_ABI = get_dict_from_string(Address_ABI)
    contractAddress = Address_ABI['contract']
    abi = Address_ABI['abi']
    wallet = Address_ABI['wallet']

    creator = getContractCreator(contractAddress)
    
    is_wallet = (wallet.lower() == creator.lower()) and creator != 'Invalid'
        
    if not isinstance(abi,dict):
        abi = get_dict_from_string(abi)
    
    contract = get_contract(contractAddress,abi)
    
    return contract,abi,is_wallet
        
def get_contract(contractAddress,abi):

    w3 = Web3(HTTPProvider('https://goerli.infura.io/v3/a6285c05a4094c4ea4a16c1395c44881'))

    try:
        contract = w3.eth.contract(address=w3.toChecksumAddress(contractAddress),abi=abi)
    except:
        contract = None
    
    return contract

def rentCar_Grader(Address_ABI):

    rentCar,abi,is_wallet = get_contract_info(Address_ABI)

    if not is_wallet:
        return 0, 'This contract was not created by your wallet'
    
    if rentCar is None:
        return 0, "Not a valid contract address"

    constructor = get_constructor(abi)
    if constructor is None:
        return 0, 'Constructor not defined in ABI\nMake sure you have supplied a valid ABI and the functions are spelled correctly and capitlization is correct'

    if len(constructor['inputs']) == 0:
        return 0, 'Constructor does not have any parameters\nMake sure you have supplied a valid ABI and the functions are spelled correctly and capitlization is correct'

    functions = ['carDetails','rentCar','returnCar','withdraw']
    for function in functions:
        if function not in get_abi_functions(abi):
            return 0, f'{function} function not defined in ABI\nMake sure it is spelled correctly and capitlization is correct'
    
    carDetails = [element['outputs'][0]['internalType'] for element in abi if 'name' in element and element['name'] == 'carDetails'][0]
    
    if 'struct' not in carDetails:
        return 0, 'carDetails function does not return a struct\n'

    try:
        _,_,_,_,rentAmt = rentCar.functions.carDetails().call({"from":myaccount})
        if isinstance(rentAmt,int):
            return 0, 'rentAmt is not a uint\n'
    except:
        rentAmt = 0
    
    try:
        tx = rentCar.functions.rentCar().call({'from':myaccount,'value':rentAmt})
        rentOk = True
    except:
        rentOk = False

    if rentAmt  > 0 and not rentOk:
        return 90, 'Not able to rent car'
    elif rentAmt > 0 and rentOk:
        return 100, 'RentCar is correct'

    return 80, 'Rental Amount not correct'

def studentID_Grader(Address_ABI):
    
    studentID,abi,is_wallet = get_contract_info(Address_ABI)

    if not is_wallet:
        return 0, 'This contract was not created by your wallet'
    
    if studentID is None:
        return 0, "Not a valid contract address"

    constructor = get_constructor(abi)
    if constructor is None:
        return 0, 'Constructor not defined in ABI\nMake sure you have supplied a valid ABI and the functions are spelled correctly and capitlization is correct'

    if len(constructor['inputs']) == 0:
        return 0, 'Constructor does not have any parameters\nMake sure you have supplied a valid ABI and the functions are spelled correctly and capitlization is correct'

    functions = ['viewMyId','updateID']
    for function in functions:
        if function not in get_abi_functions(abi):
            return 0, f'{function} function not defined in ABI\nMake sure it is spelled correctly and capitlization is correct'
    
    updateid = [element['inputs'] for element in abi if 'name' in element and element['name'] == 'updateID'][0]
    if len(updateid) == 0:
        return 0, 'updateID function does not have any parameters\n'

    try:
        id = studentID.functions.viewMyId().call({"from":myaccount})
        if not isinstance(id,int):
            return 0, 'id is not a uint\n'
    except Exception as e:
        id = 0
    
    try:
        tx = studentID.functions.updateID(23456).call({'from':myaccount})
        permitOnlyOwner = False
    except Exception as e:
        permitOnlyOwner = True

    if id > 0 and not permitOnlyOwner:
        return 90, 'updateID function does not permit only owner'
    if id > 0 and permitOnlyOwner:
        return 100, 'Student ID is correct'
    
    return 80, 'Contract does not return a valid ID'

def MidTerm_Grader(Address_ABI):

    midTerm,abi,is_wallet = get_contract_info(Address_ABI)

    if not is_wallet:
        return 0, 'This contract was not created by your wallet'
    
    if midTerm is None:
                return 0, "Not a valid contract address"
    
    constructor = get_constructor(abi)
    if constructor is None:
        return 0, 'Constructor not defined in ABI\nMake sure you have supplied a valid ABI and the functions are spelled correctly and capitlization is correct'

    if len(constructor['inputs']) == 0:
        return 0, 'Constructor does not have any parameters\nMake sure you have supplied a valid ABI and the functions are spelled correctly and capitlization is correct'

    if 'getValue' not in get_abi_functions(abi):
        return 0, 'getValue function not defined in ABI\nMake sure it is spelled correctly and capitlization is correct'
    
    if 'value' not in get_abi_functions(abi):
        return 0, 'value function not defined or not public\nMake sure it is spelled correctly and capitlization is correct'

    try:
        midTerm.functions.updates(100).call({'from':myaccount})
        return 75, f'updates function is not restricted to owner'
    except Exception as e:
        # expecting error
        pass
            
        

    try:
        value = midTerm.functions.getValue().call({"from":myaccount})
    except Exception as e:
        return 75, f"getValue function does not run correctly\nError:\n{str(e)}"

    
    if value==100:
        return 100, 'MidTerm is correct'
    elif value > 0:
        return 80, f'getValue function does not return correct value'
    
    
    return 75, f'getValue function does not return correct value'

def MyID_Grader(Address_ABI):

  
    myID,abi,is_wallet = get_contract_info(Address_ABI)
    
    if not is_wallet:
        return 0, 'This contract was not created by your wallet'
    
    if 'getID' not in get_abi_functions(abi):
        return 0, 'getID function not defined in ABI\nMake sure it is spelled correctly and capitlization is correct'

    if myID is None:
        return 0, "Not a valid contract address"

    try:
        id = myID.functions.getID().call({"from":myaccount})
    except Exception as e:
        if 'You are not approved to view this ID' in str(e):
            return 80, f'getID function does not give access to {myaccount}'
        return 0, f"getID function does not run correctly\nError:\n{str(e)}"

    
    if id == 0:
        grade,comment = 100, 'Homework is correct'
    else:
        grade,comment = 85, f'getID does not return correct elements'
    
    
    return grade,comment

def payUB_Grader(Address_ABI):
    
    payUB,UB_abi,is_wallet =  get_contract_info(Address_ABI)

    if not is_wallet:
        return 0, 'This contract was not created by your wallet'

    if 'viewMyBill' not in get_abi_functions(UB_abi):
        return 0, 'viewMyBill function not defined in ABI\nMake sure you have supplied a valid ABI and the functions are spelled correctly and capitlization is correct'

    if payUB is None:
        return 0, 'Not a valid contract address'

    try:
        billtopay = payUB.functions.billsToPay(myaccount).call()
    except:
        billtopay = -1

    try:
        mybill = payUB.functions.viewMyBill().call({"from":Web3.toChecksumAddress(myaccount)})
    except:
        mybill = -1
    
    grade, comment = 75, f'Bill to {myaccount} is not correct'
    
    if billtopay == 500 and mybill == 500:
        grade,comment = 100,'Homework is correct'
    if billtopay == 500 and mybill != 500:
        grade,comment = 85,'viewMyBill function does not return correct value'
    
    return grade,comment

def sha256_grader(submission:str) :
    
    if submission.endswith('.pdf'):
        return 0, 'Submission must be a python file'
    
    correcthash = "d6e8f9655184c6f96b24dc3df0c8eb88678181c79f4d7f809b51e88288976f7d"
    
    cwd = get_cwd()
    cwd = os.path.join(cwd,'graders','imports')
    
    shutil.copy(submission,os.path.join(cwd,'SHAIMPORT.py'))
    
    try:
        from graders.imports.SHAIMPORT import SHA256
    except Exception as e:
        error_msg = str(e).replace('SHAIMPORT.py','')
        if 'from' in error_msg:
            error_msg = error_msg[:error_msg.find('from')]
        return 0, f"Submission does not compile correctly or SHA256 function not defined.\nError:\n{error_msg} "
    
    try:
        hash = SHA256('Cesar Garcia')
    except Exception as e:
        return 0, f"SHA256 does not run correctly\nError:\n{str(e).replace('SHAIMPORT.py','')}"
        
    if hash is None:
        return 0, f"SHA256 does not run correctly, it returns None"
    
    if isinstance(hash,list):
        hash = ''.join(hash)
        
    if isinstance(hash,bytes):
        hash = hash.decode('utf-8')
        
    if hash[:2] == '0x':
        hash = hash[2:]
    
    if hash == correcthash:
        return 100, f'Hash "{hash}" is correct'
    
    if len(hash) == len(correcthash):
        return 90, f'Hash "{hash}" is not correct, it should be "{correcthash}"'

    return 80,f'Hash "{hash}" is not correct length or content, it should be "{correcthash}"'


def ecc_grader(submission:str) :
    
    if submission.endswith('.pdf'):
        return 0, 'Submission must be a python file'
    
    
    def sumPoints(Cm):

        sum = 0
        try:
            for c in Cm:
                sum += np.sum([p1+p2 for p1,p2 in c])
        except:
            sum = 0
        return sum
    
    def grade_ecc():
        
        exception_error = ''
        try:
            from graders.imports.ECCIMPORT import EllipticCurve
        except Exception as e:
            exception_error = e
            return 0, f'Error importing ECCIMPORT\n\n{str(exception_error).replace("ECCIMPORT.py",os.path.basename(submission))}'
        

        
        # Elliptic Curve 224  2^224
        p = 26959946667150639794667015087019630673557916260026308143510066298881
        a = -3
        b = 18958286285566608000408668544493926415504680968679321075787234672564
        Gx = 19277929113566293071110308034699488026831934219452440156649784352033
        Gy = 19926808758034470970197974370888749184205991990603949537637343198772
        n = 26959946667150639794667015087019625940457807714424391721682722368061

        try:
            ec = EllipticCurve(p, a, b)

            ec.set_G((Gx, Gy))  # starting point, all points defined from here

            # Get the private and public keys
            ec.set_private_key(131071)  #random prime
            ec.get_public_key()


            message = 'UB'


            Cm = ec.encode(message,k=17)

            m = ec.decode(Cm)
        except Exception as e:
            Cm = ((0,0),(0,0))
            m = ""
            exception_error=e

        if isinstance(m,list):
            m = ''.join(m)

        Cm_expected = [((19399464229459456007477471411003978864755290924325272939384776426428, 26863117366256785198219971769961599705632546399319105640204669897254), (22366613121329198004288806282357461654303397783183087425218549613485, 22170808050464581101203449810735905866030401314162623049009791623290)), ((19399464229459456007477471411003978864755290924325272939384776426428, 26863117366256785198219971769961599705632546399319105640204669897254), (26151281380560056398891667785380074997817010130475655082194580013230, 1379490757570207481338776245190580867813158616047458270168072031140))]
        correct_sum = sumPoints(Cm_expected)
            
        student_sum = sumPoints(Cm)
        
        if correct_sum == student_sum and m == "UB":
            return 100, f'Encryption succesfull'
        
        if correct_sum == student_sum:
            return 90, f'Encryptions do not match\n\nYour Encryption:\n{Cm}\n\nExpected Encryption:\n{Cm_expected} '
        
        if student_sum == 0:
            return 70, f'Encryption failed\n\n{str(exception_error).replace("ECCIMPORT.py",os.path.basename(submission))}'

        return 80,f'Your Encryption:\n{Cm}\n\nExpected Encryption:\n{Cm_expected} '

    cwd = get_cwd()
    cwd = os.path.join(cwd,'graders','imports')
    shutil.copy(submission,os.path.join(cwd,'ECCIMPORT.py'))
    points,comment = grade_ecc()
    
    return points, comment
    
def wallet_grader(submission:str) :
    # graded by form for entering wallet address
    pass


graders= {
    "SHA256": sha256_grader,
    "ECC Curve": ecc_grader,
    "Wallet": wallet_grader,
    "PayUB": payUB_Grader,
    "myID": MyID_Grader,
    "Mid Term": MidTerm_Grader,
    "Rent Car": rentCar_Grader,
    "Student ID": studentID_Grader,
}
def call_grader(assignment:str,submission:str) -> int:
   
   return graders[assignment](submission)
    
    