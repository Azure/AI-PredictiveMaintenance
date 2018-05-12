#!/bin/bash

pushd ~
wget $1
unzip AML.zip -d AML
popd

source /anaconda/bin/activate py35
conda install nbformat
conda env update --file ~/AML/aml_config/conda_dependencies.yml

pushd ~/notebooks
rm -rf *
popd

cp -r ~/AML/Notebooks ~/notebooks

mkdir ~/mnt
mkdir ~/mnt/azureml-share