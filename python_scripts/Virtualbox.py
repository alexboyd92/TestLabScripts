'''This is a script used to automate the creation of virtualbox machines 
it is defaulted to the openvas machine for this project with the ISO for
the machine named openvas and in the same directory as the script'''
## Name for the machine cannot have spaces
name="openvas"
# Read access memory for the machine in mb
ram_Size=8096
# Maximum hardive space for the machine in mb
hardrive_Size=10000
#location of the iso for the machine to run 
iso_location = "unbuntu1804-testbed-server.iso"
#Used for creating the virtual hardrive do not change this change the name value instead
location=name+"/"+name
#used to determine cpu cores
cpu_cores=4
#used to determine vram
vram=128
import os

## Create and register virtualbox
os.system("VBoxManage createvm --name "+name+" --ostype Ubuntu_64 --register")
## Allocate RAM
os.system("VBoxManage modifyvm "+name+"  --memory "+str(ram_Size)+" --vram "+str(vram))
## Create SATA Controller
os.system("VBoxManage storagectl "+name+"  --name \"SATA Controller\" --add sata --controller IntelAhci")
# Create a virtual hard drive of name and size specified
os.system("VBoxManage createhd --filename VirtualBox\ VMs/"+location+".vdi --size "+str(hardrive_Size)+" --format VDI")
# Attach the hardrive to the virtual machine
os.system("VBoxManage storageattach "+name+" --storagectl \"SATA Controller\" --port 0 --device 0 --type hdd --medium VirtualBox\ VMs/"+location+".vdi")
# create controller for the iso
os.system("VBoxManage storagectl "+name+" --name \"IDE Controller\" --add ide --controller PIIX4")
#Attach the iso 
os.system("VBoxManage storageattach "+name+" --storagectl \"IDE Controller\" --port 1 --device 0 --type dvddrive --medium "+iso_location)
#Start the system
os.system("VBoxManage startvm "+name)
