echo OFF

for /f "tokens=*" %%i in ('dir "D:\program files (x86)\SiteExtensions\Kudu\" /s /b ^| findstr /i nuget\.exe$') do set NUGET_EXE=%%i
"%NUGET_EXE%" install -Source https://www.siteextensions.net/api/v2/ -OutputDirectory D:\home\site\tools python364x64 

for /f "tokens=*" %%i in ('dir "D:\home\site\tools\" /b') do set PYTHON_VERSION=%%i
XCOPY /E /H /Y /C "d:\home\site\tools\%PYTHON_VERSION%\content\python364x64\*" "d:\home\site\tools\"

python.exe -m pip install -r d:\home\site\wwwroot\setupPython\requirements.txt
