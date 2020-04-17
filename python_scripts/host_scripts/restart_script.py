import subprocess
def runCommand(bashCommand):
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()
	return 0
# updates/ upgrades all programs
def update():
	restart = "sudo reboot"
	date = "echo restart completed on: ; date"
	runCommand(restart)
	
	runCommand(date)

	return 0

def  main():
	update()
	



	return 0	

if __name__ == '__main__':
	main()
