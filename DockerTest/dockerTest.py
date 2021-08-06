import subprocess
import sys

s = subprocess.check_output('docker ps', shell=True)
print ('Results of docker ps' + str(s))