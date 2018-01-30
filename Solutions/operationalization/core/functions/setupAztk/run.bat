echo OFF

pushd d:\home\site\tools\
git clone https://www.github.com/azure/aztk
cd aztk
git checkout 85a472c591a46597d4a9fbf1ee6c796184499a3a
python -m pip install -e .
popd
