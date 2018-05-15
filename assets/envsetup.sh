#!/bin/bash

pushd ~
wget $1
unzip AML.zip -d AML
popd

pushd ~/notebooks
rm -rf *
popd

pushd ~
unzip ~/AML.zip -d ~/notebooks
popd

source /anaconda/bin/activate py35
conda install nbformat
conda env update --file ~/AML/aml_config/conda_dependencies.yml

mkdir ~/mnt
mkdir ~/mnt/azureml-share