set READY_FILE=D:\home\site\READY

IF EXIST %READY_FILE% EXIT

mkdir D:\home\site\jars
D:\home\python364x64\python.exe -m pip install pip
D:\home\python364x64\python.exe -m pip install --upgrade -r D:\home\site\wwwroot\requirements.txt
D:\home\python364x64\python.exe -m pip install D:\home\site\wwwroot\shared_modules
D:\home\python364x64\python.exe run.py
echo. > %READY_FILE%
EXIT %errorlevel%
