@echo off

set DEDOP_HOME=%~dpnx0\..

echo.
@echo Welcome to the DeDop command-line interface. Type "dedop -h" to get help.
echo.

PATH=%DEDOP_HOME%\Scripts;%PATH%

prompt $G$S

cmd /K ""