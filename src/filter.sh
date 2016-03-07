#!/bin/bash

gacc="$1"
duration="$2"
filter="$3"
outputf="$4"

gy=${gacc/.acc/.y}
log=${gacc/.acc/.log}
heap="1g"
ambicmd="java -Xss8m -Xmx1g -jar $(pwd)/AmbiDexter.jar"

acc_to_yacc(){
  cat $gacc | grep  "%token" | sed -e 's/,//g' -e 's/;$//' > $gy
  echo "" >> $gy
  cat $gacc | grep -v '%token' | sed -e 's/%nodefault/\n%%/' >> $gy
}

acc_to_yacc
/usr/bin/timeout $duration $ambicmd -q -pg -h -${filter} -${outputf} $gy > $log 2>&1 || exit $?

outg=$(grep 'Exporting grammar to' $log | sed -e 's/Exporting grammar to //')
echo "$outg"

