#!/bin/bash

# View extension logs by running
# sudo cat /var/log/azure/Microsoft.OSTCExtensions.CustomScriptForLinux/1.5.2.2/extension.log
# (the version may be different)

user=`awk -F: '$3 >= 1000 {print $1, $6}' /etc/passwd | tail -n 1`
echo $user
username=${user% *}
homedir=${user#* }

basedir=`dirname $0`

cp $basedir/envsetup.sh $homedir/

sudo -u $username bash $homedir/envsetup.sh $1 $2 $3
sudo cp $homedir/AML/config/spark-defaults.config /dsvm/tools/spark/current/conf/spark-defaults.conf
sudo mkdir $homedir/mnt
sudo mkdir $homedir/mnt/azureml-share
sudo cp $homedir/AML/config/envvariable.sh /etc/profile.d/envvariable.sh
sudo mount -t cifs //$2.file.core.windows.net/azureml-share $homedir/mnt/azureml-share -o vers=3.0,username=$2,password=$3,dir_mode=0777,file_mode=0777,serverino
sudo chmod -R a+rwx $homedir/mnt/azureml-share

    sudo echo 'export AZUREML_NATIVE_SHARE_DIRECTORY="/home/laks/mnt/azureml-share"' >> /etc/environment
    sudo echo "export TELEMETRY_STORAGE_ACCOUNT_NAME=$2" >> /etc/environment
    sudo echo "export TELEMETRY_STORAGE_ACCOUNT_KEY=$3" >> /etc/environment
    sudo echo "export STAGING_STORAGE_ACCOUNT_NAME=$2" >> /etc/environment
    sudo echo "export STAGING_STORAGE_ACCOUNT_KEY=$3" >> /etc/environment
    sudo echo 'export TELEMETRY_CONTAINER_NAME="telemetry"' >> /etc/environment
