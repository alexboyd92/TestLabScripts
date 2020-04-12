''' Script to start the openvas virtualmachine'''
# get subprocces
import subprocess
# this lets us not have to worry about dictonarys with subprocces you can just give it a string
def runCommand(bashCommand):
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return 0
def main():
    runCommand("VBoxManage startvm openvas")
## this makes main run
if __name__ == '__main__':
    main()
