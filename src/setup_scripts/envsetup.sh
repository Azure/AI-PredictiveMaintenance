#!/bin/bash


pushd ~/notebooks
rm -rf *
popd

source /anaconda/bin/activate py35
conda install nbformat
conda env update --file ~/notebooks/aml_config/conda_dependencies.yml

mkdir ~/mnt
mkdir ~/mnt/azureml-share