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

sudo -u $username bash $homedir/envsetup.sh $1 $2
