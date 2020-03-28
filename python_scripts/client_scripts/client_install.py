import subprocess



def runCommand(bashCommand):
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()
	return 0

def update():
	update = "sudo apt-get update -y"
	upgrade = "sudo apt-get upgrade -y"
	runCommand(update)
	print ("update complete")
	runCommand(upgrade)
	print ("upgrade complete")
	return 0


def installVBox():
	getKey = "wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo apt-key add -"
	getKey2 = "wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | sudo apt-key add -"
	getRepo = 'sudo add-apt-repository "deb http://download.virtualbox.org/virtualbox/debian bionic contrib"'
	getVbox = 'sudo apt-get install virtualbox'

	runCommand(getKey)
	runCommand(getKey2)
	runCommand(getRepo)
	print ("vbox repo setup complete")
	update()
	runCommand(getVbox)
	print ("Vbox Installed")

	return 0 


def  main():
	update()
	installVBox()
	update()

	return 0	

if __name__ == '__main__':
	main()


