import subprocess
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

def  main():
	update()
	# this is to be used once gvminstall is up and working properly
	# 4/22/20 gvm install is not able to work properly
	#exec(open('gvminstall.py').read())



	return 0	

if __name__ == '__main__':
	main()
