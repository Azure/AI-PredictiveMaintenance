set READY_FILE=D:\home\site\READY
set READY_FILE_2=D:\home\site\READY2

IF NOT EXIST %READY_FILE% EXIT

IF EXIST %READY_FILE_2% EXIT

D:\home\python364x64\python.exe run.py

echo. > %READY_FILE_2%
