from webproject.modules.web3_interface import  getContractCreator, get_contract
import json
import shutil
import os
import numpy as np
from webproject.modules.dotenv_util import get_cwd

UPLOADPATH = os.getenv("UPLOADPATH")
STOREPATH = os.getenv("STOREPATH")
myaccount = os.getenv("MYWALLET")

class Functions:
    def __init__(self,name:str,inputs:list[str]=[],outputs:list[str]=[],is_ownable:bool=False):
        self.name:str = name
        self.inputs:list[str] = inputs
        self.outputs:list[str] = outputs
        self.is_ownable:bool = is_ownable
        

class Contracts_Grader:
    
    def __init__(self,Address_ABI:dict={},has_constructor:bool=False,constructor_has_inputs:bool=False):
        self.grader = grader
        self.grade:int = 0
        self.msg:str = ''
        self.contract:int = None
        self.abi:dict = None
        self.is_wallet:bool = False
        self.Address_ABI:dict = None
        self.Address_ABI:dict = Address_ABI
        self.has_constructor:bool = has_constructor
        self.constructor_has_inputs:bool = constructor_has_inputs
        
    def functions(self,functions:list[Functions]=[])->None:
        self.functions:Functions = functions
        return 
    def get_dict_from_string(self,dictstring)->dict:
        try:
            _dict = json.loads(dictstring.replace('\t','').replace('\n',''))
        except Exception as e:
            _dict = {}
            
        return _dict

    def get_abi_functions(self):
    
        return [i['name'] for i in self.abi if i['type'] == 'function']

    def has_constructor(self):
        return 'constructor' in [i['type'] for i in self.abi]
    
    def get_constructor(self):
        constructor_arr = [i for i in self.abi if i['type'] == 'constructor']
        constructor = constructor_arr[0] if len(constructor_arr) > 0 else None
        return constructor

    def get_contract_info(self)->None:
        
        self.Address_ABI = self.get_dict_from_string(self.Address_ABI)
        contractAddress = self.Address_ABI['contract']
        self.abi = self.Address_ABI['abi']
        self.wallet = self.Address_ABI['wallet']

        creator = getContractCreator(contractAddress)
        
        is_wallet = (self.wallet.lower() == creator.lower()) and creator != 'Invalid'
            
        if not isinstance(self.abi,dict):
            self.abi = self.get_dict_from_string(self.abi)
        
        self.contract = get_contract(contractAddress,self.abi)
        
        return None

    def call_function(self,function:Functions)->None:
        if function.is_ownable:
            try:
                self.contract.functions[function.name](*function.inputs).call({'from':self.wallet})
                self.grade,self.msg = 75, f'{function.name} function  callable by others than owner'
                return False
            except Exception as e:
                return True
        
        test_outputs = self.contract.functions[function.name](*function.inputs).call({'from':self.wallet})
        test_outputs = list(test_outputs) if isinstance(test_outputs,tuple) else [test_outputs]
        
        if test_outputs != function.outputs:
            self.grade,self.msg = 75, f'{function.name} does not return correct values'
            return False
        
        return True
    
    def check_contract(self):
        
        self.get_contract_info()

        # if not self.is_wallet:
        #     self.grade,self.msg =  0, 'This contract was not created by your wallet'
        #     return False
        
        if self.contract is None:
            self.grade,self.msg = 0, "Not a valid contract address"
            return False

        if self.has_constructor:
            constructor = self.get_constructor()
            if constructor is None:
               self.grade,self.msg = 0, 'Constructor not defined in ABI\nMake sure you have supplied a valid ABI and the functions are spelled correctly and capitlization is correct'
               return False

            if self.constructor_has_inputs and len(constructor['inputs']) == 0:
                self.grade,self.msg = 0, 'Constructor does not have any parameters\nMake sure you have supplied a valid ABI and the functions are spelled correctly and capitlization is correct'
                return False


        for function in self.functions:
            if function.name not in self.get_abi_functions():
                self.grade,self.msg = 0, f'{function.name} function not defined in ABI\nMake sure it is spelled correctly and capitlization is correct'
                return False
            if not self.call_function(function):
                return False
        
        self.grade,self.msg = 100, 'Assignment completed successfully'
        return True

def rentCar_Grader(Address_ABI:dict):
    
    contract = Contracts_Grader(None,Address_ABI,has_constructor=True,constructor_has_inputs=True)
    contract.functions([
        Functions('carDetails',outputs=['make','model','year','doors','rentAmt']),
        Functions('rentCar',outputs=[12345]),
        Functions('retunrCar',outputs=[12345]),
        Functions('withdraw',outputs=[],is_ownable=True)
    ])
    
    contract.check_contract()
    
    carDetails = [element['outputs'][0]['internalType'] for element in contract.abi if 'name' in element and element['name'] == 'carDetails'][0]
    
    if 'struct' not in carDetails:
        contract.grade, contract.msg = 0, 'carDetails function does not return a struct\n'
    
    try:
        tx = contract.contract.functions.rentCar().call({'from':myaccount,'value':rentAmt})
        rentOk = True
    except:
        rentOk = False
        
    return contract.grade,contract.msg
    

def studentID_Grader(Address_ABI:dict):
    
    contract = Contracts_Grader(None,Address_ABI,has_constructor=True,constructor_has_inputs=True)
    contract.functions(['viewMyId','updateID'])
    
    if not contract.check_contract():
        return contract.grade,contract.msg
    
        
    updateid = [element['inputs'] for element in contract.abi if 'name' in element and element['name'] == 'updateID'][0]
    if len(updateid) == 0:
        return 0, 'updateID function does not have any parameters\n'

    try:
        id = contract.contract.functions.viewMyId().call({"from":myaccount})
        if not isinstance(id,int):
            return 0, 'id is not a uint\n'
    except Exception as e:
        id = 0
    
    try:
        tx = contract.contract.functions.updateID(23456).call({'from':myaccount})
        permitOnlyOwner = False
    except Exception as e:
        permitOnlyOwner = True

    if id > 0 and not permitOnlyOwner:
        return 90, 'updateID function does not permit only owner'
    if id > 0 and permitOnlyOwner:
        return 100, 'Student ID is correct'
    
    return 80, 'Contract does not return a valid ID'

def MidTerm_Grader(Address_ABI:dict):
    
    contract = Contracts_Grader(Address_ABI,has_constructor=True,constructor_has_inputs=True)
    contract.functions([
        Functions('getValue',outputs=[100]),
        Functions('updates',inputs=[200],is_ownable=True),
        Functions('value',outputs=[100])
    ])
    
    contract.check_contract()
    
    return contract.grade,contract.msg
    

def MyID_Grader(Address_ABI:dict):
    
    contract = Contracts_Grader(Address_ABI,has_constructor=True,constructor_has_inputs=True)
    contract.functions(['getID'])
    
    if not contract.check_contract():
        return contract.grade,contract.msg
    
    try:
        id = contract.contract.functions.getID().call({"from":myaccount})
    except Exception as e:
        if 'You are not approved to view this ID' in str(e):
            return 80, f'getID function does not give access to {myaccount}'
        return 0, f"getID function does not run correctly\nError:\n{str(e)}"

    
    if id == 0:
        grade,comment = 100, 'Homework is correct'
    else:
        grade,comment = 85, f'getID does not return correct elements'
    
    
    return grade,comment

def payUB_Grader(Address_ABI:dict):
    
    contract = Contracts_Grader(Address_ABI,has_constructor=True,constructor_has_inputs=True)
    contract.functions(['viewMyBill'])
    
    if not contract.check_contract():
        return contract.grade,contract.msg
    
    try:
        billtopay = contract.contract.functions.billsToPay(myaccount).call()
    except:
        billtopay = -1

    try:
        mybill = contract.contract.functions.viewMyBill().call({"from":myaccount})
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
    
def wallet_grader(submission:str=None) :
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
    
    