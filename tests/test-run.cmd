
if exist %~dp0venv/Scripts/python.exe  goto :run_watcher

:install_depedencies
"C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\python.exe" -m pip install --user virtualenv
"C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\python.exe" -m virtualenv %~dp0venv
%~dp0venv/Scripts/pip.exe install watchdog
%~dp0venv/Scripts/pip.exe install mapactionpy_controller

:run_watcher
%~dp0venv/Scripts/python.exe %~dp0../cmf_watcher/cmf_watcher.py "D:\code\github\cmf_watcher\tests\testdir\20YYiso3nn\cmf_description.json"
::%~dp0../cmf_watcher/tests/testdir/20YYiso3nn/cmf_description.json

