#!/bin/bash

# build ACCENT
wget http://accent.compilertools.net/accent.tar -O ~/accent.tar
tar xf ~/accent.tar -C ~/
(cd ~/accent/accent && ./build)

# apply patch for entire -- essentially sets up an exit code
wget https://raw.githubusercontent.com/nvasudevan/experiment/master/patches/entire.c.patch -O ~/entire.c.patch
patch -b -p0 ~/accent/entire/entire.c < ~/entire.c.patch
