'''Quick script to disconnect the internal network and reconnect to a NAT network with internet '''
import subprocess
from time import sleep

def runCommand(bashCommand):
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return 0
def main():
    #turn off innternal network
    runCommand("VBoxManage modifyvm openvas --cableconnected1 off")
#sleep for two seconds just in case
    sleep(2)
    #turn on NAT network for internet
    runCommand("VBoxManage modifyvm openvas  --cableconnected2 on")
if __name__ == '__main__':
    main()

