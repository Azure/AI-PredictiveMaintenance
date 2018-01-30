echo OFF

rem TODO: implement nuget.exe discovery so that this works no matter what Kudu version is installed
"D:\Program Files (x86)\SiteExtensions\Kudu\70.10119.3222\bin\Scripts\nuget.exe" install -Source https://www.siteextensions.net/api/v2/ -OutputDirectory D:\home\site\tools python364x64 
XCOPY /E /H /Y /C "d:\home\site\tools\python364x64.3.6.4.1\content\python364x64\*" "d:\home\site\tools\"

python.exe -m pip install -r d:\home\site\wwwroot\setupPython\requirements.txt

