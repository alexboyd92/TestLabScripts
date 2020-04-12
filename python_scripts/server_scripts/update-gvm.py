''' Quick script to update the server system'''
  
  # get the os command
  import os 
  # update ubuntu
  os.system("sudo apt update")
  #upgrade ubuntu
  os.system("sudo apt upgrade -y")
  #run nvt sync
  os.system("greenbone-nvt-sync") 
  #set user id to gvm
  os.setuid(1001)
  #run scapdata and certdata sync
  os.system("greenbone-certdata-sync ;greenbone-scapdata-sync")

