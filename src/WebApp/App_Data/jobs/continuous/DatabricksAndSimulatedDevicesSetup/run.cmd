set READY_FILE=D:\home\site\READY
set FINISH_FILE=D:\home\site\FINISH

IF NOT EXIST %FINISH_FILE% EXIT
IF NOT EXIST %READY_FILE% EXIT

D:\home\python364x64\python.exe simulated_devices_setup.py
D:\home\python364x64\python.exe run.py
echo. > %FINISH_FILE%

