#!/bin/bash

THIS_DIR=$(dirname "$0")
THIS_PYTHON=${THIS_DIR}/python

rm -rf ${THIS_PYTHON}

echo ========================================================
echo Installing Python...
echo ========================================================
conda create -y -p ${THIS_PYTHON} python=3
source activate ${THIS_PYTHON}

echo ========================================================
echo Installing dependencies...
echo ========================================================
conda install -y numpy scipy netCDF4
conda install -y -c IOOS basemap matplotlib jupyter

echo ========================================================
echo Installing DeDop...
echo ========================================================
(
    cd ../..
    python setup.py clean --all install
)
# see
# https://github.com/pypa/setuptools/issues/272
# '--executable' does njot work for generated 'console_scripts'
sed -i "1c#!/usr/bin/env python" ${THIS_PYTHON}/bin/dedop

echo ========================================================
echo Building installer...
echo ========================================================
# TODO
#makensis dedop-installer.nsi

echo ========================================================
echo Done!
echo ========================================================
