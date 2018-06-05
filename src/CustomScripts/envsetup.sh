#!/bin/bash

source /anaconda/bin/activate py35
conda install nbformat
conda env update --file ~/notebooks/aml_config/conda_dependencies.yml

#to install ggplot in DSVM uncomment the following
#conda remove -n py35 -y pandas
#conda install -n py35 -y pandas==0.20.3
#conda install -n py35 -y -c conda-forge ggplot

conda install -n py35 -y python-snappy
pip install imblearn

pip install --upgrade --extra-index-url https://azuremlsdktestpypi.azureedge.net/sdk-release/Preview/E7501C02541B433786111FE8E140CAA1 azureml-sdk

mkdir ~/mnt
mkdir ~/mnt/azureml-share
