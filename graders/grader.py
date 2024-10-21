from webproject.modules.web3_interface import getContractCreator,get_contract
from web3 import Web3,HTTPProvider
import json
import shutil
import os
import numpy as np
from webproject.modules.dotenv_util import get_cwd
import re
from graders.grade_foundry import grade_foundry
from graders.grade_final import gradeFinal
from graders.MidTermExam import get_exam

UPLOADPATH = os.getenv("UPLOADPATH")
STOREPATH = os.getenv("STOREPATH")
myaccount = os.getenv("MYWALLET")


def check_anvil_running() -> None:
    w3 = Web3(Web3.HTTPProvider(os.getenv("ANVIL_PROVIDER")))
    my_address = os.getenv("ANVIL_ACCOUNT")
    if not w3.is_connected():
        raise Exception("ANVIL is not running")

def get_dict_from_string(dictstring:str) -> dict:
    try:
        dict = json.loads(dictstring)
    except Exception as e:
        dict = {}
        
    return dict

def get_abi_functions(abi:dict) :
   
    return [i['name'] for i in abi if i['type'] == 'function']

def has_constructor(abi:dict) -> bool:
    return 'constructor' in [i['type'] for i in abi]
   
def get_constructor(abi:dict) -> list[str]:
    constructor_arr = [i for i in abi if i['type'] == 'constructor']
    constructor = constructor_arr[0] if len(constructor_arr) > 0 else None
    return constructor

def get_contract_info(Address_ABI:str) -> tuple[str,str,bool]:
    
    Address_ABI = get_dict_from_string(Address_ABI)
    contractAddress = Address_ABI['contract']
    abi = Address_ABI['abi']
    wallet = Address_ABI['wallet']
    network = Address_ABI['network'] if 'network' in Address_ABI else 'sepolia'

    creator = getContractCreator(contractAddress,network)
    
    is_wallet = (wallet.lower() == creator.lower()) and creator != 'Invalid'
    # is_wallet = True     
    if not isinstance(abi,dict):
        abi = get_dict_from_string(abi)
    
    contract = get_contract(contractAddress,abi,network)
    
    return contract,abi,is_wallet
        
def rentCar_Grader(Address_ABI:str) -> tuple[int,str]:

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
        if not isinstance(rentAmt,int):
            return 0, 'rentAmt is not a uint\n'
    except:
        rentAmt = 0
    
    try:
        tx = rentCar.functions.rentCar().call({'from':myaccount,'value':rentAmt})
        rentOk = True
    except Exception as e:
        rentOk = False

    if rentAmt  > 0 and not rentOk:
        return 90, 'Not able to rent car'
    elif rentAmt > 0 and rentOk:
        return 100, 'RentCar is correct'

    return 80, 'Rental Amount not correct'

def studentID_Grader(Address_ABI: str) -> tuple[int,str]:
    
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

def MidTerm_Grader(Address_ABI:str) -> tuple[int,str]:

    midterm,abi,is_wallet = get_contract_info(Address_ABI)

    
    if not is_wallet:
        return 0, 'This contract was not created by your wallet'
    
    if midterm is None:
                return 0, "Not a valid contract address, or problem connecting to contract"
    
    student_id = get_dict_from_string(Address_ABI)['user_id']['student_id']
    exam = get_exam(student_id)
    
    constructor = get_constructor(abi)
    grade = 70
    msg = ''

    if constructor is None:
        msg += 'Constructor not defined in ABI\nMake sure you have supplied a valid ABI and the functions are spelled correctly and capitlization is correct'

    if len(constructor['inputs']) != len(exam['Structure']['properties']):
        msg += 'Constructor does not have the correct parameters\nMake sure you have supplied a valid ABI and the functions are spelled correctly and capitlization is correct'

    for idx,inp in enumerate(constructor['inputs']):
        if inp['type'] != exam['Structure']['properties'][idx]['type']:
            msg += 'Constructor does not have the correct parameters\nMake sure you have supplied a valid ABI and the functions are spelled correctly and capitlization is correct'
        

    functions_to_verify = [exam['get_function'],exam['variable'],exam['update_function']]

    for func in functions_to_verify:
        if func not in get_abi_functions(abi):
            msg += f"{func} function not defined or not public\nMake sure it is spelled correctly and capitlization is correct"
        else:
            grade += 5
    # grade == 55 here
    try:
        midterm.functions[exam['update_function']](100).call({'from':myaccount})
        msg +=  f'Updates function is not restricted to owner'
    except Exception as e:
        if 'execution reverted' not in e.args[0]:
            msg +=  f'Error in updates function\n{str(e)}'
        else:
            grade += 5

    try:
        value = midterm.functions[exam['get_function']]().call({"from":myaccount})
        grade += 5
    except Exception as e:
        msg += f"getValue function does not run correctly\nError:\n{str(e)}"

    if len(value) != len(exam['Structure']['properties']):
        msg += "value does not return correct number of elements"
    grade += 5
    
    
    return grade, f'Great work on your mid term exam!!' if msg == '' else msg

def MyID_Grader(Address_ABI) -> tuple[int,str]:

  
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

    
    if id[2] == 123456:
        grade,comment = 100, 'Homework is correct'
    else:
        grade,comment = 85, f'getID does not return correct elements'
    
    
    return grade,comment

def payUB_Grader(Address_ABI) -> tuple[int,str]:
    
    payUB,UB_abi,is_wallet =  get_contract_info(Address_ABI)

    if not is_wallet:
        return 0, 'This contract was not created by your wallet'

    if payUB is None:
        return 0, 'Not a valid contract address'
    
    grade = 55
    comment = ''
    ab_functions = get_abi_functions(UB_abi)
    for func in ['addBill','viewBill','withdraw','payBill']:
        if func not in ab_functions:
            comment +=  f'{func} function not defined in ABI\nMake sure you have supplied a valid ABI and the functions are spelled correctly and capitlization is correct\n'
            continue
        grade += 5

    try:
        mybill = payUB.functions.viewBill().call({"from":Web3.to_checksum_address(myaccount)})
    except:
        mybill = -1
    
    
    if mybill == 500:
        grade += 25
    else:
        comment += f'Bill to student {myaccount} should be 500'
    
    comment = 'Homework is Correct' if grade == 100 else comment
    
    return grade,comment

def web3_grader(submission:str) -> tuple[int,str]:
    from graders.grade_web3 import grade_web3
    
    check_anvil_running()
    grade, msg = grade_web3(submission,'./src/Interact.py')

                
    return grade, msg
    

def wallet_grader(submission:str) -> tuple[int,str] :
    # graded by form for entering wallet address
    pass

def token_grader(Address_ABI:str) -> tuple[int,str]:
    ubtoken,token_abi,is_wallet =  get_contract_info(Address_ABI)

    if not is_wallet:
        return 0, 'This contract was not created by your wallet'

    functions_needed = ['name','symbol','totalSupply','balanceOf','decimals']
    msg = ''
    for f in functions_needed:
        if f not in get_abi_functions(token_abi):
            msg += f'{f} function not defined in ABI'
    if msg != '':
        return 0, msg + '\nMake sure you have supplied a valid ABI and the functions are spelled correctly and capitlization is correct'
    

    if ubtoken is None:
        return 0, 'Not a valid contract address'
    try:
        name = ubtoken.functions.name().call()
        symbol = ubtoken.functions.symbol().call()
        totalSupply = ubtoken.functions.totalSupply().call()
        tokenbalance = ubtoken.functions.balanceOf(myaccount).call()
        decimals = ubtoken.functions.decimals().call()
    except:
        return 0, 'Error calling functions'
    
    msg = ''
    base_grade = 75
    if name == "UBStudent":
        base_grade += 5
    else:
        msg += 'Name is not UBStudent\n'
    if symbol == "US":
        base_grade += 5
    else:
        msg += 'Symbol is not US\n'
    if totalSupply == 10_000_000 * 10**decimals:
        base_grade += 5
    else:
        msg += 'Total Supply is not 10,000,000\n'
    if tokenbalance == 1000 * 10**decimals:
        base_grade += 10
    else:
        msg += f'Balance in {myaccount} is not 1,000\n'
        
    return base_grade, msg

def nft_grader(Address_ABI:str) -> tuple[int,str]:
    ubnft,token_abi,is_wallet =  get_contract_info(Address_ABI)

    if not is_wallet:
        return 0, 'This contract was not created by your wallet'

    functions_needed = ['name','symbol','tokenURI']
    msg = ''
    for f in functions_needed:
        if f not in get_abi_functions(token_abi):
            msg += f'{f} function not defined in ABI'
    if msg != '':
        return 0, msg + '\nMake sure you have supplied a valid ABI and the functions are spelled correctly and capitlization is correct'
    

    if ubnft is None:
        return 0, 'Not a valid contract address'
    try:
        name = ubnft.functions.name().call()
        symbol = ubnft.functions.symbol().call()
        uris = []
        for x in range(3):
            uris.append(ubnft.functions.tokenURI(x).call())
    except Exception as e:
        return 0, 'Error calling functions'
    
    msg = ''
    base_grade = 80
    if name >= "":
        base_grade += 5 
    else:
        msg += 'Name is not Populated\n'
    if symbol >= "":
        base_grade += 5
    else:
        msg += 'Symbol is not Populated\n'
    if len(uris) == 3:
        base_grade += 10
    else:
        msg += '3 NFTs were not minted\n'
        
    return base_grade, msg

graders= {
    "Wallet": wallet_grader,
    "PayUB": payUB_Grader,
    "myID": MyID_Grader,
    "Mid Term": MidTerm_Grader,
    "Rent Car": rentCar_Grader,
    "Student ID": studentID_Grader,
    "web3_py": web3_grader,
    "Foundry": grade_foundry,
    "token": token_grader,
    "nft": nft_grader,
    "Final Project": gradeFinal,
}
def call_grader(assignment:str,submission:str) -> tuple[int,str]:
   
   return graders[assignment](submission)
    
    

if __name__ == '__main__':
    web3_grader('https://github.com/Gypsaman/web3-tutorial.git')