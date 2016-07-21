@echo off

set THIS_DIR=%~dp0
set THIS_PYTHON=%THIS_DIR%\python

@echo ========================================================
@echo Installing Python...
@echo ========================================================
call conda create -y -p %THIS_PYTHON% python=3
call activate %THIS_PYTHON%

@echo ========================================================
@echo Installing dependencies...
@echo ========================================================
call conda install -y numpy scipy netcdf4
call conda install -y pyproj matplotlib bokeh jupyter ipywidgets

@echo ========================================================
@echo Installing DeDop...
@echo ========================================================
cd %THIS_DIR%\..\..
call python setup.py clean --all
call python setup.py install

call dedop --version > installer\win\version.txt
SET /p DEDOP_VERSION=<installer\win\version.txt

@echo ========================================================
@echo Building installer...
@echo ========================================================
cd %THIS_DIR%
call makensis dedop-installer.nsi

@echo ========================================================
@echo Done!
@echo ========================================================
