'''Quick script to disconnect gvm from internet and reconnect to the internal network'''
import subprocess
from time import sleep
#disable internet
subprocess.run(["VBoxManage","modifyvm","openvas","--cableconnected2","off"])
#enable the connection to the internal network
subprocess.run(["VBoxManage","modifyvm","openvas","--cableconnected1","on"])
def runCommand(bashCommand):
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return 0
def main():
    #turn off NAT network
    runCommand("VBoxManage modifyvm openvas --cableconnected2 off")
    #sleep just to make sure they are not on at the same time
    sleep(2)

    #turn on internal network
    runCommand("VBoxManage modifyvm openvas  --cableconnected1 on")
if __name__ == '__main__':
    main()
