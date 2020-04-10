import os
import pwd
import subprocess
from pwd import getpwnam
import subprocess

def runCommand(bashCommand):
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return 0
def main():
    #install dependencies first
    runCommand('sudo apt update')
    runCommand('sudo apt install -y software-properties-common')
    runCommand('sudo add-apt-repository universe')

    runCommand('sudo apt install -y cmake pkg-config libglib2.0-dev libgpgme11-dev libgnutls28-dev uuid-dev libssh-gcrypt-dev \
    libldap2-dev doxygen graphviz libradcli-dev libhiredis-dev libpcap-dev bison libksba-dev libsnmp-dev \
    gcc-mingw-w64 heimdal-dev libpopt-dev xmltoman redis-server xsltproc libical2-dev postgresql \
    postgresql-contrib postgresql-server-dev-all gnutls-bin nmap rpm nsis curl wget fakeroot gnupg \
    sshpass socat snmp smbclient libmicrohttpd-dev libxml2-dev python-polib gettext \
    python3-paramiko python3-lxml python3-defusedxml python3-pip python3-psutil virtualenv ')

    runCommand('sudo apt install -y texlive-latex-extra --no-install-recommends')
    runCommand('sudo apt install -y texlive-fonts-recommended ')

    runCommand('curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add - ')
    runCommand('echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list')


    runCommand('sudo apt -y install yarn')

    print("Creating gvm user account")
    runCommand('cp /etc/environment ~/environment.bak')
    runCommand('sudo sed -i \'s|PATH="|PATH="/opt/gvm/bin:/opt/gvm/sbin:/opt/gvm/.local/bin:|g\' /etc/environment ')

    runCommand('sudo bash -c \'cat << EOF > /etc/ld.so.conf.d/gvm.conf \n'
             '/opt/gvm/lib \n'
             'EOF\'')

    #if directory exists skip creating dir
    pathExists = os.path.exists('/opt/gvm')
    if not pathExists :
        print(pathExists)
        runCommand('sudo mkdir /opt/gvm')
    #end if

    #if user exists skip creating
    try:
        pwd.getpwnam('gvm')
    except KeyError:
        runCommand('sudo adduser gvm --disabled-password --home /opt/gvm/ --no-create-home --gecos \'\' ')

    runCommand('sudo usermod -aG redis gvm')
    runCommand('sudo chown gvm:gvm /opt/gvm/')

    #run the next section of commands as gvm
    ###########################################
    runCommand('sudo -u gvm mkdir /opt/gvm/src')
    os.chdir("/opt/gvm/src")

    runCommand('sudo su gvm -c "export PKG_CONFIG_PATH=/opt/gvm/lib/pkgconfig:$PKG_CONFIG_PATH "')

    #GET GVM Installers
    runCommand('sudo -u gvm wget -O gvm-libs-11.0.0.tar.gz  https://github.com/greenbone/gvm-libs/archive/v11.0.0.tar.gz')
    runCommand('sudo -u gvm wget -O openvas-7.0.0.tar.gz https://github.com/greenbone/openvas/archive/v7.0.0.tar.gz ')
    runCommand('sudo -u gvm wget -O gvmd-9.0.0.tar.gz https://github.com/greenbone/gvmd/archive/v9.0.0.tar.gz')
    runCommand('sudo -u gvm wget -O openvas-smb-1.0.5.tar.gz https://github.com/greenbone/openvas-smb/archive/v1.0.5.tar.gz')
    runCommand('sudo -u gvm wget -O gsa-9.0.0.tar.gz https://github.com/greenbone/gsa/archive/v9.0.0.tar.gz')
    runCommand('sudo -u gvm wget -O ospd-openvas-1.0.0.tar.gz https://github.com/greenbone/ospd-openvas/archive/v1.0.0.tar.gz ')
    runCommand('sudo -u gvm wget -O ospd-2.0.0.tar.gz https://github.com/greenbone/ospd/archive/v2.0.0.tar.gz')

    runCommand('sudo -u gvm find . -name \\*.gz -exec tar zxvfp {} \\;')



    #install gvm-libs
    os.chdir("/opt/gvm/src/gvm-libs-11.0.0")
    runCommand('sudo su gvm -c "export PKG_CONFIG_PATH=/opt/gvm/lib/pkgconfig:$PKG_CONFIG_PATH "')
    runCommand('sudo -u gvm mkdir /opt/gvm/src/gvm-libs-11.0.0/build')
    os.chdir("/opt/gvm/src/gvm-libs-11.0.0/build")
    runCommand('sudo -u gvm cmake -DCMAKE_INSTALL_PREFIX=/opt/gvm .. ')
    runCommand('sudo -u gvm make')
    runCommand('sudo -u gvm make doc')
    runCommand('sudo -u gvm make install')


    runCommand('sudo su root -c "cp /opt/gvm/lib/pkgconfig/*.pc /usr/lib/pkgconfig/"')


    #install openvas smb
    os.chdir("/opt/gvm/src/openvas-smb-1.0.5")
    runCommand('sudo su gvm -c "export PKG_CONFIG_PATH=/opt/gvm/lib/pkgconfig:$PKG_CONFIG_PATH "')
    runCommand('sudo -u gvm mkdir /opt/gvm/src/openvas-smb-1.0.5/build')
    os.chdir("/opt/gvm/src/openvas-smb-1.0.5/build")
    runCommand('sudo -u gvm cmake -DCMAKE_INSTALL_PREFIX=/opt/gvm .. ')
    runCommand('sudo -u gvm make')
    runCommand('sudo -u gvm make doc')
    runCommand('sudo -u gvm make install')

    os.chdir("/opt/gvm/src/openvas-7.0.0")
    runCommand('sudo su gvm -c "export PKG_CONFIG_PATH=/opt/gvm/lib/pkgconfig:$PKG_CONFIG_PATH "')
    runCommand('sudo -u gvm mkdir /opt/gvm/src/openvas-7.0.0/build')
    os.chdir("/opt/gvm/src/openvas-7.0.0/build")
    runCommand('sudo -u gvm cmake -DCMAKE_INSTALL_PREFIX=/opt/gvm .. ')
    runCommand('sudo -u gvm make')
    runCommand('sudo -u gvm make doc')
    runCommand('sudo -u gvm make install')


    ###########################################
    #end GVM user section

    #section ran as root.
    runCommand('sudo su root -c ldconfig')
    runCommand('sudo su root -c "cp /etc/redis/redis.conf /etc/redis/redis.orig "')
    runCommand('sudo su root -c "cp /opt/gvm/src/openvas-7.0.0/config/redis-openvas.conf /etc/redis/" ')
    runCommand('sudo su root -c "chown redis:redis /etc/redis/redis-openvas.conf "')
    runCommand('sudo su root -c "echo \"db_address = /run/redis-openvas/redis.sock\" > /opt/gvm/etc/openvas/openvas.conf "')
    runCommand('sudo su root -c "systemctl enable redis-server@openvas.service" ')
    runCommand('sudo su root -c "systemctl start redis-server@openvas.service"')

    runCommand('sudo su root -c "sysctl -w net.core.somaxconn=1024"')
    runCommand('sudo su root -c "sysctl vm.overcommit_memory=1"')

    runCommand('sudo su root -c "echo \"net.core.somaxconn=1024\"  >> /etc/sysctl.conf"')
    runCommand('sudo su root -c "echo \"vm.overcommit_memory=1\" >> /etc/sysctl.conf"')

    #cpy service
    runCommand('sudo su root -c "cp /opt/gvm/services/disable-thp.service /etc/systemd/system/disable-thp.service"')

    runCommand('sudo su root -c "systemctl daemon-reload"')
    runCommand('sudo su root -c "systemctl start disable-thp"')
    runCommand('sudo su root -c "systemctl enable disable-thp"')
    runCommand('sudo su root -c "systemctl restart redis-server"')

    #############################################
    #Copy Sudoers file
    runCommand('sudo su root -c "mv /home/openvas/Documents/_files/sudoers /etc/sudoers"')
    ############################################
    #section ran as GVM USER
    runCommand('sudo su gvm -c "greenbone-nvt-sync"')
    runCommand('sudo su gvm -c "openvas -u"')

    #install GVMD v9.0.0
    os.chdir("/opt/gvm/src/gvmd-9.0.0")
    runCommand('sudo su gvm -c "export PKG_CONFIG_PATH=/opt/gvm/lib/pkgconfig:$PKG_CONFIG_PATH "')
    runCommand('sudo -u gvm mkdir /opt/gvm/src/gvmd-9.0.0/build')
    os.chdir("/opt/gvm/src/gvmd-9.0.0/build")
    runCommand('sudo -u gvm cmake -DCMAKE_INSTALL_PREFIX=/opt/gvm .. ')
    runCommand('sudo -u gvm make')
    runCommand('sudo -u gvm make doc')
    runCommand('sudo -u gvm make install')


    ############################################
    #postgresql configuration

    runCommand('sudo -u postgres bash')
    runCommand('createuser -DRS gvm')
    runCommand('createdb -O gvm gvmd')
    runCommand('psql gvmd')
    runCommand('create role dba with superuser noinherit;')
    runCommand('grant dba to gvm;')
    runCommand('create extension "uuid-ossp";')

    ############################################


    runCommand('sudo su gvm -c "gvm-manage-certs -a"')
    runCommand('sudo su gvm -c "gvmd --create-user=admin --password=admin"')

    runCommand('sudo su gvm -c "greenbone-certdata-sync"')
    runCommand('sudo su gvm -c  "greenbone-scapdata-sync"')

     #install gsa v9.0
    os.chdir("/opt/gvm/src/gsa-9.0.0")
    runCommand('sudo su gvm -c "export PKG_CONFIG_PATH=/opt/gvm/lib/pkgconfig:$PKG_CONFIG_PATH "')
    runCommand('sudo -u gvm mkdir /opt/gvm/src/gsa-9.0.0/build')
    os.chdir("/opt/gvm/src/gsa-9.0.0/build")
    runCommand('sudo -u gvm cmake -DCMAKE_INSTALL_PREFIX=/opt/gvm .. ')
    runCommand('sudo -u gvm make')
    runCommand('sudo -u gvm make doc')
    runCommand('sudo -u gvm make install')
    ############################################

    ##OSPD-OPENVAS
    runCommand('sudo su gvm -c "export PKG_CONFIG_PATH=/opt/gvm/lib/pkgconfig:$PKG_CONFIG_PATH"')
    runCommand('sudo su gvm -c "virtualenv --python python3.6  /opt/gvm/bin/ospd-scanner/ "')
    runCommand('sudo su gvm -c "source /opt/gvm/bin/ospd-scanner/bin/activate"')

    os.chdir("/opt/gvm/src/ospd-2.0.0")
    runCommand('sudo su gvm -c "pip3 install ."')

    os.chdir("/opt/gvm/src/ospd-openvas-1.0.0")
    runCommand('sudo su gvm -c "pip3 install ."')

    ############################################
    #SERVICES
    runCommand('sudo su root -c "cp /home/openvas/Documents/_files/gvmd.service /etc/systemd/system/gvmd.service"')
    runCommand('sudo su root -c "cp /home/openvas/Documents/_files/gsad.service /etc/systemd/system/gsad.service"')
    runCommand('sudo su root -c "cp /home/openvas/Documents/_files/ospd-openvas.service  /etc/systemd/system/ospd-openvas.service "')

    runCommand('sudo su root -c "systemctl daemon-reload"')
    runCommand('sudo su root -c "systemctl enable gvmd"')
    runCommand('sudo su root -c "systemctl enable gsad"')
    runCommand('sudo su root -c "systemctl enable ospd-openvas"')
    runCommand('sudo su root -c "systemctl start gvmd"')
    runCommand('sudo su root -c "systemctl start gsad"')
    runCommand('sudo su root -c "systemctl start ospd-openvas"')
    ############################################
    #register Scanner
    runCommand('sudo su gvm -c "gvmd --modify-scanner=08b69003-5fc2-4037-a479-93b440211c73 --scanner-host=/opt/gvm/var/run/ospd.sock"')
    ##end
    if __name__ == '__main__':
        main()
