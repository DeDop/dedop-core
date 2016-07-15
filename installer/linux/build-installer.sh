#!/bin/bash

THIS_DIR=$(dirname "$0")
THIS_PYTHON=${THIS_DIR}/python

rm -rf ${THIS_PYTHON}
rm -rf ${DISTRIBUTION}
rm -f ${DISTRIBUTION}.zip

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
# '--executable' doesn't work for generated 'console_scripts'
sed -i "1c#!/usr/bin/env python" ${THIS_PYTHON}/bin/dedop

DEDOP_VERSION=$(${THIS_PYTHON}/bin/python ${THIS_PYTHON}/bin/dedop --version)
KERNEL=$(uname -s)
case ${KERNEL} in
    Linux)  ARCH=linux ;;
    Darwin) ARCH=macos ;;
    *)      ARCH=other ;;
esac

echo ========================================================
echo "Building installer for version ${DEDOP_VERSION}"
echo ========================================================

DISTRIBUTION="dedop-${DEDOP_VERSION}"
mkdir ${DISTRIBUTION}
(
    cd ${DISTRIBUTION}
    ln -s ../python .
    ln -s ../dedop-shell.sh .
    ln -s ../../../LICENSE .
    echo "${DEDOP_VERSION}" > VERSION
)
zip -rv ${DISTRIBUTION}-${ARCH}.zip ${DISTRIBUTION}

echo ========================================================
echo Done!
echo ========================================================
