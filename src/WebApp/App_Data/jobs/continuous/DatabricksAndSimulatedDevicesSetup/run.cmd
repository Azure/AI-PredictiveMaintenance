set READY_FILE=D:\home\site\READY
set FINISH_FILE=D:\home\site\FINISH

IF EXIST %FINISH_FILE% EXIT
IF NOT EXIST %READY_FILE% EXIT

D:\home\python364x64\python.exe simulated_devices_setup.py
D:\home\python364x64\python.exe run.py
if %ERRORLEVEL% == 0 (
    echo. > %FINISH_FILE%
)

