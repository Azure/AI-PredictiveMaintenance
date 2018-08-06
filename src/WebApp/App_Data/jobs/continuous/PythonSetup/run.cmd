set READY_FILE=D:\home\site\wwwroot\READY

IF EXIST %READY_FILE% EXIT

mkdir D:\home\site\jars
D:\home\python364x64\python.exe -m pip install --upgrade pip
D:\home\python364x64\python.exe -m pip install --upgrade -r D:\home\site\wwwroot\requirements.txt
D:\home\python364x64\python.exe -m pip install D:\home\site\wwwroot\shared_modules
echo. > %READY_FILE%
EXIT %errorlevel%
