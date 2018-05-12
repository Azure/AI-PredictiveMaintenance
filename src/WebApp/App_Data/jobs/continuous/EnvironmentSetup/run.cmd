set READY_FILE=D:\home\site\wwwroot\READY

IF EXIST %READY_FILE% EXIT

D:\home\python364x64\python.exe -m pip install --upgrade -r D:\home\site\wwwroot\requirements.txt

D:\home\python364x64\python.exe init.py

echo. > %READY_FILE%
