#!/bin/bash

# View extension logs by running
# sudo cat /var/log/azure/Microsoft.OSTCExtensions.CustomScriptForLinux/1.5.2.2/extension.log
# (the version may be different)

user=`awk -F: '$3 >= 1000 {print $1, $6}' /etc/passwd | tail -n 1`
echo $user
username=${user% *}
homedir=${user#* }

basedir=$PWD

pushd $homedir/notebooks
rm -rf *
unzip $basedir/Notebooks.zip
chown $username:$username *
popd

source /anaconda/bin/activate py35

pip install --upgrade pip

#to install ggplot in DSVM uncomment the following
#conda remove -n py35 -y pandas
#conda install -n py35 -y pandas==0.20.3
#conda install -n py35 -y -c conda-forge ggplot

conda install -n py35 -y python-snappy
pip install imblearn
pip install --upgrade --extra-index-url https://azuremlsdktestpypi.azureedge.net/sdk-release/Preview/E7501C02541B433786111FE8E140CAA1 azureml-sdk
pip install --upgrade databricks-cli

touch $homedir/.databrickscfg
cat << EOF > $homedir/.databrickscfg
[DEFAULT]
host = $2
token = $3
EOF
