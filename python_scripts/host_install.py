# allows for use of bash scripts
import subprocess
#protects password imputs so they are not palin text
import getpass
# import os module 
import os 
  

gitHub_address = 'https://github.com/alexboyd92/TestLabScripts.git'
localFileLocation = '/home/snacker/cs4900/openvas/testFileReplace/replace.txt'
localGit = '/home/snacker/cs4900/openvas/git_repo/'
replacefile = '/home/snacker/cs4900/openvas/git_repo/TestLabScripts/test_py/test_replacefile'
homeDir = '/home/snacker/'
install = 'sudo apt-get install '
# runs a bash command
def runCommand(bashCommand):
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()
	return 0
# updates/ upgrades all programs
def update():
	update = "sudo apt-get update -y"
	upgrade = "sudo apt-get upgrade -y"
	runCommand(update)
	print ("update complete")
	runCommand(upgrade)
	print ("upgrade complete")
	return 0

#installs virtualbox
def installVBox():
	getKey = "wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo apt-key add -"
	getKey2 = "wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | sudo apt-key add -"
	getRepo = 'sudo add-apt-repository "deb http://download.virtualbox.org/virtualbox/debian bionic contrib"'
	getVbox = install + 'virtualbox'

	runCommand(getKey)
	runCommand(getKey2)
	runCommand(getRepo)
	print ("vbox repo setup complete")
	update()
	runCommand(getVbox)
	print ("Vbox Installed")

	return 0 

# installs git
def installGit():
	getGit = install+'git'
	print('installing git')
	runCommand(getGit)
	print('git Installed')
	return 0

# grabs files from github and places them into the correct spots
def configDHCP(gitUser, gitPass):
	# auto inputs username/ password
	getConfigFiles = 'sudo git clone'+gitUser+':'+gitPass+'@'+ gitHub_address
	#testing
	#getConfigFiles = 'sudo git clone '+ gitHub_address
	print('configuring your DHCP Server')
	installGit()
	os.chdir(localGit)  
	runCommand('git init')
	print("git initilaized")
	runCommand(getConfigFiles)
	os.system('cp '+replacefile+' '+localFileLocation)
	print('DHCP Server configured')
	os.chdir(homeDir)

#installs DHCP server
def installDHCP():
	getDHCP = install + 'isc-dhcp-server'
	print('installing a DHCP Server')
	runCommand(getDHCP)
	print('DHCP Server installed')
	return 0


def installOpenssh():
	getssh = install + 'openssh-server'
	print('installing openssh')
	runCommand(getssh)
	print('openssh installed')
	return 0

def startDHCP():
	start = 'sudo systemctl start isc-dhcp-server.service'
	enable = 'sudo systemctl enable isc-dhcp-server.service'
	runCommand(start)
	runCommand(enable)
	print('DHCP is started and set up to restart on boot')

	return 0

def configIP():
	'sudo nano /etc/network/interfaces'
	localFileLocation = '/etc/network/interfaces'
	replacefile = '/home/snacker/cs4900/openvas/git_repo/TestLabScripts/config/interfaces'
	print('configuring Ip settings')
	os.system('cp '+replacefile+' '+localFileLocation)
	print('Ip settings configured')
	return 0

def  main():
	gitUser = input('github Username:')
	gitPass = getpass.getpass(prompt='github password:', stream=None) 
	update()
	installVBox()
	installOpenssh()
	installDHCP()
	configDHCP(gitUser, gitPass)
	configIP()
	startDHCP()
	update()

	return 0	

if __name__ == '__main__':
	main()


