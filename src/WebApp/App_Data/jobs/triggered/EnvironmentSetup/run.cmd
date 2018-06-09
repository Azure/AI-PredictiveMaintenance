set READY_FILE=D:\home\site\wwwroot\READY

mkdir D:/home/site/jars
D:\home\python364x64\python.exe -m pip install --upgrade pip
D:\home\python364x64\python.exe -m pip install --upgrade -r D:\home\site\wwwroot\requirements.txt
D:\home\python364x64\python.exe init.py
echo. > %READY_FILE%
EXIT %errorlevel%
