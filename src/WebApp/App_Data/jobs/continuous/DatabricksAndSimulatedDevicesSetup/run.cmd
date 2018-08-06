set READY_FILE=D:\home\site\READY

IF NOT EXIST %READY_FILE% EXIT

D:\home\python364x64\python.exe simulated_devices_setup.py
D:\home\python364x64\python.exe run.py

