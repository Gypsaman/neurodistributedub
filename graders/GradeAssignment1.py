import os
import shutil
import numpy as np

studentfiles = os.path.join(os.getcwd(),'StudentFiles')

def grade(submission:str) -> int:
    cwd = os.getcwd()
    cwd = os.path.join(cwd,'neurodistributedub') if cwd = '\home\neurodistributed' else cwd
    shutil.copy(submission,os.path.join(cwd,'SHAIMPORT.py'))
    from SHAIMPORT import SHA256
    correcthash = "3f24ef2774456a4aad63f8b1f8772c89a0b498965b400e09a869be5769e514f8"
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

def hashfile():
    from SHA256 import SHA256
    with open('SHAIMPORT.py','r') as f:
        content = f.read()
    return SHA256(content)



def base_results():
    
    import SHA256
    print(results(SHA256))
    import SHAIMPORT
    print(results(SHAIMPORT))

def results(module):

    val = 0x84c87814
    funcs = {k:(f,False) for k,f in vars(module).items() if callable(f)}
    functions = {
        'stringtobits':["cesar"],
        'Pack32Bits':[np.ones(32,dtype=np.int8)],
        'preprocess':["cesar"],
        'rightshift':(val,2),
        'leftshift':(val,2),
        'rightrotate':(val,2),
        'leftrotate':(val,2)
    }
    results = {}
    for func,arg in functions.items():
        if func in vars(module):
            r = vars(module)[func](*arg)
            funcs[func] = (funcs[func][0],True)
        else:
            r = None
        results[func] = (arg,r)
    
    return results

if __name__ == '__main__':

    grade_all()
    
