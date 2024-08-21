import subprocess
import os

cwd = os.getcwd()
os.chdir('../foundry/payUB')
result = subprocess.run(['forge','test','--match-path','payUB.t.sol'],stdout=subprocess.PIPE)
print(result.stdout.decode('utf-8'))
os.chdir(cwd)

