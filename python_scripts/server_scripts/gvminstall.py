import os
import pwd
import subprocess
from pwd import getpwnam

#install dependencies first
os.system('sudo apt install -y software-properties-common')
os.system('sudo add-apt-repository universe')

os.system('sudo apt install -y cmake pkg-config libglib2.0-dev libgpgme11-dev libgnutls28-dev uuid-dev libssh-gcrypt-dev \
libldap2-dev doxygen graphviz libradcli-dev libhiredis-dev libpcap-dev bison libksba-dev libsnmp-dev \
gcc-mingw-w64 heimdal-dev libpopt-dev xmltoman redis-server xsltproc libical2-dev postgresql \
postgresql-contrib postgresql-server-dev-all gnutls-bin nmap rpm nsis curl wget fakeroot gnupg \
sshpass socat snmp smbclient libmicrohttpd-dev libxml2-dev python-polib gettext \
python3-paramiko python3-lxml python3-defusedxml python3-pip python3-psutil virtualenv ')

os.system('sudo apt install -y texlive-latex-extra --no-install-recommends')
os.system('sudo apt install -y texlive-fonts-recommended ')

os.system('curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add - ')
os.system('echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list')

os.system('sudo apt update')
os.system('sudo apt -y install yarn')

print("Creating gvm user account")
os.system('cp /etc/environment ~/environment.bak')
os.system('sudo sed -i \'s|PATH="|PATH="/opt/gvm/bin:/opt/gvm/sbin:/opt/gvm/.local/bin:|g\' /etc/environment ')

os.system('sudo bash -c \'cat << EOF > /etc/ld.so.conf.d/gvm.conf \n'
         '/opt/gvm/lib \n'
         'EOF\'')

#if directory exists skip creating dir
pathExists = os.path.exists('/opt/gvm')
if not pathExists :
    print(pathExists)
    os.system('sudo mkdir /opt/gvm')
#end if

#if user exists skip creating
try:
    pwd.getpwnam('gvm')
except KeyError:
    os.system('sudo adduser gvm --disabled-password --home /opt/gvm/ --no-create-home --gecos \'\' ')

os.system('sudo usermod -aG redis gvm')
os.system('sudo chown gvm:gvm /opt/gvm/')

#run the next section of commands as gvm
###########################################
os.system('sudo -u gvm mkdir /opt/gvm/src')
os.chdir("/opt/gvm/src")

os.system('sudo su gvm -c "export PKG_CONFIG_PATH=/opt/gvm/lib/pkgconfig:$PKG_CONFIG_PATH "')

#GET GVM Installers
os.system('sudo -u gvm wget -O gvm-libs-11.0.0.tar.gz  https://github.com/greenbone/gvm-libs/archive/v11.0.0.tar.gz')
os.system('sudo -u gvm wget -O openvas-7.0.0.tar.gz https://github.com/greenbone/openvas/archive/v7.0.0.tar.gz ')
os.system('sudo -u gvm wget -O gvmd-9.0.0.tar.gz https://github.com/greenbone/gvmd/archive/v9.0.0.tar.gz')
os.system('sudo -u gvm wget -O openvas-smb-1.0.5.tar.gz https://github.com/greenbone/openvas-smb/archive/v1.0.5.tar.gz')
os.system('sudo -u gvm wget -O gsa-9.0.0.tar.gz https://github.com/greenbone/gsa/archive/v9.0.0.tar.gz')
os.system('sudo -u gvm wget -O ospd-openvas-1.0.0.tar.gz https://github.com/greenbone/ospd-openvas/archive/v1.0.0.tar.gz ')
os.system('sudo -u gvm wget -O ospd-2.0.0.tar.gz https://github.com/greenbone/ospd/archive/v2.0.0.tar.gz')

os.system('sudo -u gvm find . -name \\*.gz -exec tar zxvfp {} \\;')



#install gvm-libs
os.chdir("/opt/gvm/src/gvm-libs-11.0.0")
os.system('sudo su gvm -c "export PKG_CONFIG_PATH=/opt/gvm/lib/pkgconfig:$PKG_CONFIG_PATH "')
os.system('sudo -u gvm mkdir /opt/gvm/src/gvm-libs-11.0.0/build')
os.chdir("/opt/gvm/src/gvm-libs-11.0.0/build")
os.system('sudo -u gvm cmake -DCMAKE_INSTALL_PREFIX=/opt/gvm .. ')
os.system('sudo -u gvm make')
os.system('sudo -u gvm make doc')
os.system('sudo -u gvm make install')


os.system('sudo su root -c "cp /opt/gvm/lib/pkgconfig/*.pc /usr/lib/pkgconfig/"')


#install openvas smb
os.chdir("/opt/gvm/src/openvas-smb-1.0.5")
os.system('sudo su gvm -c "export PKG_CONFIG_PATH=/opt/gvm/lib/pkgconfig:$PKG_CONFIG_PATH "')
os.system('sudo -u gvm mkdir /opt/gvm/src/openvas-smb-1.0.5/build')
os.chdir("/opt/gvm/src/openvas-smb-1.0.5/build")
os.system('sudo -u gvm cmake -DCMAKE_INSTALL_PREFIX=/opt/gvm .. ')
os.system('sudo -u gvm make')
os.system('sudo -u gvm make doc')
os.system('sudo -u gvm make install')

os.chdir("/opt/gvm/src/openvas-7.0.0")
os.system('sudo su gvm -c "export PKG_CONFIG_PATH=/opt/gvm/lib/pkgconfig:$PKG_CONFIG_PATH "')
os.system('sudo -u gvm mkdir /opt/gvm/src/openvas-7.0.0/build')
os.chdir("/opt/gvm/src/openvas-7.0.0/build")
os.system('sudo -u gvm cmake -DCMAKE_INSTALL_PREFIX=/opt/gvm .. ')
os.system('sudo -u gvm make')
os.system('sudo -u gvm make doc')
os.system('sudo -u gvm make install')


###########################################
#end GVM user section

#section ran as root.
os.system('sudo su root -c ldconfig')
os.system('sudo su root -c "cp /etc/redis/redis.conf /etc/redis/redis.orig "')
os.system('sudo su root -c "cp /opt/gvm/src/openvas-7.0.0/config/redis-openvas.conf /etc/redis/" ')
os.system('sudo su root -c "chown redis:redis /etc/redis/redis-openvas.conf "')
os.system('sudo su root -c "echo \"db_address = /run/redis-openvas/redis.sock\" > /opt/gvm/etc/openvas/openvas.conf "')
os.system('sudo su root -c "systemctl enable redis-server@openvas.service" ')
os.system('sudo su root -c "systemctl start redis-server@openvas.service"')

os.system('sudo su root -c "sysctl -w net.core.somaxconn=1024"')
os.system('sudo su root -c "sysctl vm.overcommit_memory=1"')

os.system('sudo su root -c "echo \"net.core.somaxconn=1024\"  >> /etc/sysctl.conf"')
os.system('sudo su root -c "echo \"vm.overcommit_memory=1\" >> /etc/sysctl.conf"')

#cpy service
os.system('sudo su root -c "cp /opt/gvm/services/disable-thp.service /etc/systemd/system/disable-thp.service"')

os.system('sudo su root -c "systemctl daemon-reload"')
os.system('sudo su root -c "systemctl start disable-thp"')
os.system('sudo su root -c "systemctl enable disable-thp"')
os.system('sudo su root -c "systemctl restart redis-server"')

#############################################
#Copy Sudoers file
os.system('sudo su root -c "mv /home/openvas/Documents/_files/sudoers /etc/sudoers"')
############################################
#section ran as GVM USER
os.system('sudo su gvm -c "greenbone-nvt-sync"')
os.system('sudo su gvm -c "openvas -u"')

#install GVMD v9.0.0
os.chdir("/opt/gvm/src/gvmd-9.0.0")
os.system('sudo su gvm -c "export PKG_CONFIG_PATH=/opt/gvm/lib/pkgconfig:$PKG_CONFIG_PATH "')
os.system('sudo -u gvm mkdir /opt/gvm/src/gvmd-9.0.0/build')
os.chdir("/opt/gvm/src/gvmd-9.0.0/build")
os.system('sudo -u gvm cmake -DCMAKE_INSTALL_PREFIX=/opt/gvm .. ')
os.system('sudo -u gvm make')
os.system('sudo -u gvm make doc')
os.system('sudo -u gvm make install')

'''
############################################
#postgresql configuration

os.system('sudo -u postgres bash')
os.system('createuser -DRS gvm')
os.system('createdb -O gvm gvmd')
os.system('psql gvmd')
os.system('create role dba with superuser noinherit;')
os.system('grant dba to gvm;')
os.system('create extension "uuid-ossp";')

############################################


os.system('sudo su gvm -c "gvm-manage-certs -a"')
os.system('sudo su gvm -c "gvmd --create-user=admin --password=admin"')

os.system('sudo su gvm -c "greenbone-certdata-sync"')
os.system('sudo su gvm -c  "greenbone-scapdata-sync"')

 #install gsa v9.0
os.chdir("/opt/gvm/src/gsa-9.0.0")
os.system('sudo su gvm -c "export PKG_CONFIG_PATH=/opt/gvm/lib/pkgconfig:$PKG_CONFIG_PATH "')
os.system('sudo -u gvm mkdir /opt/gvm/src/gsa-9.0.0/build')
os.chdir("/opt/gvm/src/gsa-9.0.0/build")
os.system('sudo -u gvm cmake -DCMAKE_INSTALL_PREFIX=/opt/gvm .. ')
os.system('sudo -u gvm make')
os.system('sudo -u gvm make doc')
os.system('sudo -u gvm make install')
############################################

##OSPD-OPENVAS
os.system('sudo su gvm -c "export PKG_CONFIG_PATH=/opt/gvm/lib/pkgconfig:$PKG_CONFIG_PATH"')
os.system('sudo su gvm -c "virtualenv --python python3.6  /opt/gvm/bin/ospd-scanner/ "')
os.system('sudo su gvm -c "source /opt/gvm/bin/ospd-scanner/bin/activate"')

os.chdir("/opt/gvm/src/ospd-2.0.0")
os.system('sudo su gvm -c "pip3 install ."')

os.chdir("/opt/gvm/src/ospd-openvas-1.0.0")
os.system('sudo su gvm -c "pip3 install ."')

############################################
#SERVICES
os.system('sudo su root -c "cp /home/openvas/Documents/_files/gvmd.service /etc/systemd/system/gvmd.service"')
os.system('sudo su root -c "cp /home/openvas/Documents/_files/gsad.service /etc/systemd/system/gsad.service"')
os.system('sudo su root -c "cp /home/openvas/Documents/_files/ospd-openvas.service  /etc/systemd/system/ospd-openvas.service "')

os.system('sudo su root -c "systemctl daemon-reload"')
os.system('sudo su root -c "systemctl enable gvmd"')
os.system('sudo su root -c "systemctl enable gsad"')
os.system('sudo su root -c "systemctl enable ospd-openvas"')
os.system('sudo su root -c "systemctl start gvmd"')
os.system('sudo su root -c "systemctl start gsad"')
os.system('sudo su root -c "systemctl start ospd-openvas"')
############################################
#register Scanner
os.system('sudo su gvm -c "gvmd --modify-scanner=08b69003-5fc2-4037-a479-93b440211c73 --scanner-host=/opt/gvm/var/run/ospd.sock"')
##end
'''
