#!/bin/bash -x

# run sinbad against a example grammar

# build ACCENT
wget http://accent.compilertools.net/accent.tar -O ~/accent.tar
tar xf ~/accent.tar -C ~/
(cd ~/accent/accent && ./build)

# apply patch for entire -- essentially sets up an exit code
wget https://raw.githubusercontent.com/nvasudevan/experiment/master/patches/entire.c.patch -O ~/entire.c.patch
patch -b -p0 ~/accent/entire/entire.c < ~/entire.c.patch

export ACCENT_DIR=${HOME}/accent
echo $ACCENT_DIR

pwd
# run sinbad against various backends on an example grammar
python src/sinbad -b dynamic1 -d 10 bin/amb2.acc bin/general.lex
