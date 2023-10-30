@echo off
setlocal

:: Get the directory of the current batch file
set "DIR=%~dp0"

:: Remove trailing backslash (if any) from DIR
set "DIR=%DIR:~0,-1%"

:: Add the directory to the PATH environment variable
for /f "tokens=*" %%a in ('echo %PATH%') do setx PATH "%%a;%DIR%"

:: Output result
echo The path %DIR% has been added to the PATH environment variable.

endlocal
