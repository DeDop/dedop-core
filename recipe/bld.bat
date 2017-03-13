%PYTHON% setup.py install
if errorlevel 1 exit 1

set MENU_DIR=%PREFIX%\Menu
IF NOT EXIST (%MENU_DIR%) mkdir %MENU_DIR%

set SCRIPTS_DIR=%PREFIX%\Scripts
IF NOT EXIST (%SCRIPTS_DIR%) mkdir %SCRIPTS_DIR%

copy %RECIPE_DIR%\dedop.ico %MENU_DIR%
if errorlevel 1 exit 1

copy %RECIPE_DIR%\dedop-menu-win.json %MENU_DIR%\dedop.json
if errorlevel 1 exit 1

copy %RECIPE_DIR%\dedop-shell.bat %SCRIPTS_DIR%
if errorlevel 1 exit 1

