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

userid=`id -u $username`
groupid=`id -g $username`

pushd $homedir/notebooks
rm -rf *
popd

sudo mount -t cifs //$2.file.core.windows.net/azureml-project $homedir/notebooks -o vers=3.0,username=$2,password=$3,uid=$userid,gid=$groupid,rw,dir_mode=0777,file_mode=0777,serverino

sudo -u $username bash $homedir/envsetup.sh $1 $2 $3
sudo cp $homedir/notebooks/config/spark-defaults.config /dsvm/tools/spark/current/conf/spark-defaults.conf

sudo mount -t cifs //$2.file.core.windows.net/azureml-share $homedir/mnt/azureml-share -o vers=3.0,username=$2,password=$3,uid=$userid,gid=$groupid,rw,dir_mode=0777,file_mode=0777,serverino

sudo echo "os.environ['AZUREML_NATIVE_SHARE_DIRECTORY']=\"${homedir}/mnt/azureml-share/\"" >> /etc/jupyterhub/jupyterhub_config.py
sudo echo "os.environ['TELEMETRY_STORAGE_ACCOUNT_NAME']=\"$2\"" >> /etc/jupyterhub/jupyterhub_config.py
sudo echo "os.environ['TELEMETRY_STORAGE_ACCOUNT_KEY']=\"$3\"" >> /etc/jupyterhub/jupyterhub_config.py
sudo echo "os.environ['STAGING_STORAGE_ACCOUNT_NAME']=\"$2\"" >> /etc/jupyterhub/jupyterhub_config.py
sudo echo "os.environ['STAGING_STORAGE_ACCOUNT_KEY']=\"$3\"" >> /etc/jupyterhub/jupyterhub_config.py
sudo echo 'os.environ["TELEMETRY_CONTAINER_NAME"]="telemetry"' >> /etc/jupyterhub/jupyterhub_config.py
sudo echo 'c.Spawner.env_keep.extend(["AZUREML_NATIVE_SHARE_DIRECTORY", "TELEMETRY_STORAGE_ACCOUNT_NAME", "TELEMETRY_STORAGE_ACCOUNT_KEY", "STAGING_STORAGE_ACCOUNT_NAME", "STAGING_STORAGE_ACCOUNT_KEY", "TELEMETRY_CONTAINER_NAME"])' >> /etc/jupyterhub/jupyterhub_config.py
sudo echo "c.Spawner.notebook_dir = \"$homedir/notebooks/Notebooks\"" >> /etc/jupyterhub/jupyterhub_config.py

sudo systemctl restart jupyterhub
