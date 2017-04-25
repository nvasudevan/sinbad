#!/bin/bash -x

# run sinbad against an example grammar
export ACCENT_DIR=${HOME}/accent
echo $ACCENT_DIR

depth=10
wgt=0.1

# run sinbad against various backends on an example grammar
python src/sinbad -b dynamic1 -d $depth bin/amb2.acc bin/general.lex
python src/sinbad -b dynamic2 -d $depth bin/amb2.acc bin/general.lex
python src/sinbad -b dynamic3 -d $depth bin/amb2.acc bin/general.lex
python src/sinbad -b dynamic4 -d $depth bin/amb2.acc bin/general.lex
python src/sinbad -b dynamic1rws -d $depth -w $wgt bin/amb2.acc bin/general.lex
python src/sinbad -b dynamic2rws -d $depth -w $wgt bin/amb2.acc bin/general.lex
python src/sinbad -b dynamic2fd  -d $depth -w $wgt bin/amb2.acc bin/general.lex
