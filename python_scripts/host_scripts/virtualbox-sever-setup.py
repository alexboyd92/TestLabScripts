'''This is a script used to automate the creation of virtualbox machines
it is defaulted to the openvas machine for this project with the ISO for
the machine named openvas and in the same directory as the script'''

import subprocess

def runCommand(bashCommand):
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return 0
def buildBox(name,ram_Size,iso_location,location,cpu_cores,vram,hardrive_Size,adapter):

        ## Create and register virtualbox
        runCommand("VBoxManage createvm --name "+name+" --ostype Ubuntu_64 --register")
        ## Allocate RAM
        runCommand("VBoxManage modifyvm "+name+"  --memory "+str(ram_Size)+" --vram "+str(vram))
        ## Create SATA Controller
        runCommand("VBoxManage storagectl "+name+"  --name SATA --add sata --controller IntelAhci")
        # Create a virtual hard drive of name and size specified
        runCommand("VBoxManage createhd --filename "+location+".vdi --size "+str(hardrive_Size)+" --format VDI")
        # Attach the hardrive to the virtual machine
        runCommand("VBoxManage storageattach "+name+" --storagectl SATA  --port 0 --device 0 --type hdd --medium "+location+".vdi")
        # create controller for the iso
        runCommand("VBoxManage storagectl "+name+" --name IDE-Controller --add ide --controller PIIX4")
        #Attach the iso
        runCommand("VBoxManage storageattach "+name+" --storagectl IDE-Controller --port 1 --device 0 --type dvddrive --medium "+iso_location)
        #create network connection for local network
        runCommand("VBoxManage modifyvm "+name+" --nic2 bridged --bridgeadapter2 "+adapter)
        #disconnect the local network
        runCommand(" VBoxManage modifyvm "+name+"  --cableconnected2 off")
        #create NAT connection for internet
        runCommand("VBoxManage modifyvm "+name+" --nic1 NAT")
        #Port forwarding so localhost can ssh in
        runCommand("VBoxManage modifyvm "+name+" --natpf1 guestssh,tcp,127.0.0.1,2222,10.0.2.15,22")
        #Start the system

        runCommand("VBoxManage startvm "+name)
def main():
    ## Name for the machine cannot have spaces
    name="openvas"
    # Read access memory for the machine in mb
    ram_Size=8096
    # Maximum hardive space for the machine in mb
    hardrive_Size=10000
    #location of the iso for the machine to run
    iso_location = "unbuntu1804-testbed-server.iso"
    #Used for creating the virtual hardrive do not change this change the name value instead
    location=name+"VirtualBox_VMs/"+name
    #used to determine cpu cores
    cpu_cores=4
    #used to determine vram
    vram=128
    # name of the network adapter to the internal network
    adapter="enp2s0"
    buildBox(name,ram_Size,iso_location,location,cpu_cores,vram,hardrive_Size,adapter)

if __name__ == '__main__':
    main()
