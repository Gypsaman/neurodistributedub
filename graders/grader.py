from webproject.modules.web3_interface import get_eth_balance
from web3 import Web3,HTTPProvider
import json
import shutil
import os
import numpy as np
from webproject.modules.dotenv_util import get_cwd

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

def sha256_grader(submission:str) :
    
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
    
graders= {
    "SHA256": sha256_grader,
    "ECC Curve": ecc_grader,
    # "Wallet": wallet_grader,
}
def call_grader(assignment:str,submission:str) -> int:
   
   return graders[assignment](submission)
    
    