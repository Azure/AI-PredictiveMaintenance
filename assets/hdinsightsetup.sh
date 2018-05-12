
pushd /home/$1
sudo wget https://stgjw6kzpeckznx6.blob.core.windows.net/ai-predictivemaintenance/AML.zip
sudo unzip AML.zip -d AML
popd

source /usr/bin/anaconda/bin/activate py35
sudo /usr/bin/anaconda/bin/conda install nbformat
sudo /usr/bin/anaconda/bin/conda env update --file /home/$1/AML/aml_config/conda_dependencies.yml

sudo mkdir /home/$1/mnt
sudo mkdir /home/$1/mnt/azureml-share

userid=`id -u $1`
groupid=`id -g $1`

sudo mv /home/$1/AML/jars/spark-avro_2.11-4.0.0.jar /usr/hdp/current/spark2-client/jars/


    export AZUREML_NATIVE_SHARE_DIRECTORY="/home/${1}/mnt/azureml-share\""
    export TELEMETRY_STORAGE_ACCOUNT_NAME=$2
    export TELEMETRY_STORAGE_ACCOUNT_KEY=$3
    export STAGING_STORAGE_ACCOUNT_NAME=$2
    export STAGING_STORAGE_ACCOUNT_KEY=$3
    export TELEMETRY_CONTAINER_NAME='telemetry'

sudo mount -t cifs //$2.file.core.windows.net/azureml-share /home/$1/mnt/azureml-share -o vers=3.0,username=$2,password=$3,uid=$userid,gid=$groupid,rw,dir_mode=0777,file_mode=0777,serverino