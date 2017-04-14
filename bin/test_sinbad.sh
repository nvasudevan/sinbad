#!/bin/bash -x

# run sinbad against a example grammar
export ACCENT_DIR=${HOME}/accent
echo $ACCENT_DIR

# run sinbad against various backends on an example grammar
python src/sinbad -b dynamic1 -d 10 bin/amb2.acc bin/general.lex
python src/sinbad -b dynamic2 -d 10 bin/amb2.acc bin/general.lex
python src/sinbad -b dynamic3 -d 10 bin/amb2.acc bin/general.lex
python src/sinbad -b dynamic1rws -d 10 -w 0.1 bin/amb2.acc bin/general.lex
python src/sinbad -b dynamic2rws -d 10 -w 0.1 bin/amb2.acc bin/general.lex
