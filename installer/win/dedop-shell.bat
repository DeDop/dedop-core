@echo off

set DEDOP_HOME=%~dp0\..

echo.
@echo Welcome to the DeDop Shell. Type "dedop -h" to get help.
echo.

call "%DEDOP_HOME%\python\Scripts\activate.bat" "%DEDOP_HOME%\python"

prompt $G$S

cmd /K ""