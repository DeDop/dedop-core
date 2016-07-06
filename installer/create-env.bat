conda create --yes --copy -n dedop -c defaults -c IOOS python=3 basemap numpy scipy matplotlib jupyter netCDF4
conda create --copy -n dedop -c defaults -c IOOS python=3 basemap numpy scipy matplotlib jupyter netCDF4
activate dedop
python setup.py install