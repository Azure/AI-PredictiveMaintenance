set READY_FILE=D:\home\site\wwwroot\READY
IF NOT EXIST %READY_FILE% EXIT

D:\home\python364x64\python.exe sync.py
