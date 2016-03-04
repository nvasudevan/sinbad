#!/bin/bash

gacc="$1"
duration="$2"

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
/usr/bin/timeout $duration $ambicmd -q -pg -ik 0 $gy > $log 2>&1 || exit $?

sen=$(grep ^'ambiguous sentence' $log | sed -e 's/^ambiguous sentence: //')
echo "$sen"
