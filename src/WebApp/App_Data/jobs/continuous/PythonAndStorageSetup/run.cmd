set READY_FILE=D:\home\site\READY
set PYTHON_DIR=D:\home\python364x64\python.exe
IF NOT EXIST %PYTHON_DIR% EXIT
IF EXIST %READY_FILE% EXIT

mkdir D:\home\site\jars
D:\home\python364x64\python.exe -m pip install --upgrade pip
D:\home\python364x64\python.exe -m pip install --upgrade -r D:\home\site\wwwroot\requirements.txt
D:\home\python364x64\python.exe -m pip install D:\home\site\wwwroot\shared_modules
D:\home\python364x64\python.exe run.py
if %ERRORLEVEL% == 0 (
    echo. > %READY_FILE%
)
EXIT %errorlevel%
