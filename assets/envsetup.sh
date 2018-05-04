#!/bin/bash

pushd ~
wget $1
unzip AML.zip -d AML
popd

source /anaconda/bin/activate py35
conda install nbformat
conda env update --file ~/AML/aml_config/conda_dependencies.yml

cp -r ~/AML/Notebooks ~/notebooks
    echo 'export SPARK_CLASSPATH="/dsvm/tools/spark/current/jars/azure-storage-2.0.0.jar,/dsvm/tools/spark/current/jars/hadoop-azure-2.7.4.jar,/home/laks/AML/jars/spark-avro_2.11-4.0.0.jar"' >> ~/.bashrc
    echo 'export AZUREML_NATIVE_SHARE_DIRECTORY="/home/laks/mnt/azureml-share"' >> ~/.bashrc
    echo "export TELEMETRY_STORAGE_ACCOUNT_NAME=$2" >> ~/.bashrc
    echo "export TELEMETRY_STORAGE_ACCOUNT_KEY=$3" >> ~/.bashrc
    echo "export STAGING_STORAGE_ACCOUNT_NAME=$2" >> ~/.bashrc
    echo "export STAGING_STORAGE_ACCOUNT_KEY=$3" >> ~/.bashrc
    echo 'export TELEMETRY_CONTAINER_NAME="telemetry""' >> ~/.bashrc