set THIS_DIR=%~dpnx0
set THIS_PYTHON=%THIS_DIR%\python

conda create -y -p %THIS_PYTHON% python=3
activate %THIS_PYTHON%
conda install -y -c IOOS basemap numpy scipy matplotlib jupyter netCDF4

cd %THIS_DIR%\..\..
python setup.py install

cd %THIS_DIR%
makensis dedop-installer.nsi
