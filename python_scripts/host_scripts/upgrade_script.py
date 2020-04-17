import subprocess
def runCommand(bashCommand):
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()
	return 0
# updates/ upgrades all programs
def update():
	update = "apt-get update"
	upgrade = "apt-get -y upgrade"
	clean = "apt-get clean"
	autoremove= "apt-get -y autoremove"
	runCommand(update)
	runCommand(upgrade)
	runCommand(clean)
	runCommand(autoremove)

	return 0

def  main():
	update()
	



	return 0	

if __name__ == '__main__':
	main()
