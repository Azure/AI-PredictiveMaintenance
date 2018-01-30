#!/bin/bash

pushd ~/notebooks
rm -rf *
git clone https://github.com/wdecay/MachineLearningSamples-PredictiveMaintenance
popd

source /anaconda/bin/activate py35
conda env update --file ~/notebooks/MachineLearningSamples-PredictiveMaintenance/conda_dependencies.yml

mkdir ~/.ciqs
touch ~/.ciqs/config

printf "[STORAGE]\nACCOUNT_NAME=$1\nACCOUNT_KEY=$2" > ~/.ciqs/config
