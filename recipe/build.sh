#!/bin/bash

$PYTHON setup.py install

if [ `uname` == Darwin ]
then
    cp $RECIPE_DIR/dedop-shell.command $PREFIX/bin/
    cp -r $RECIPE_DIR/dedop-shell.app $PREFIX/bin/
    sed -i -e "s,\${PKG_VERSION},${PKG_VERSION},g"  "${PREFIX}/bin/dedop-shell.app/Contents/Info.plist"
else
    cp $RECIPE_DIR/dedop-shell.sh $PREFIX/bin
    mkdir -p  $PREFIX/share/dedop
    cp $RECIPE_DIR/dedop.desktop-template $PREFIX/share/dedop/
    cp $RECIPE_DIR/dedop.png $PREFIX/share/dedop/
fi
