@echo off

set DEDOP_BIN=%~dp0

rem Make DEDOP_HOME=%DEDOP_BIN%\.. an absolute path:
pushd .
cd %DEDOP_BIN%\..
set DEDOP_HOME=%CD%
popd

call "%DEDOP_BIN%\activate.bat" "%DEDOP_HOME%"
if errorlevel 1 exit 1

prompt $G$S

echo.
@echo Welcome to the DeDop Shell. Type "dedop -h" to get help.
echo.

cmd /K ""
