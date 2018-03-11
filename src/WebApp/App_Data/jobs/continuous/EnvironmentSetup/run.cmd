set READY_FILE=D:\home\site\wwwroot\READY

IF EXIST %READY_FILE% EXIT

D:\home\python364x64\python.exe -m pip install --upgrade -r D:\home\site\wwwroot\requirements.txt

D:\home\python364x64\python.exe init.py

pushd d:\home\site\
git clone https://www.github.com/azure/aztk
cd aztk
git checkout 85a472c591a46597d4a9fbf1ee6c796184499a3a
D:\home\python364x64\python.exe -m pip install -e .
popd
echo. > %READY_FILE%