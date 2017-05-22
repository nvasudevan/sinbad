#!/bin/bash

cfgset="${1}"

usage() {
  echo "$0 <lang|bolz|mutlang>"
  exit 1
}

[ -z "$cfgset" ] && usage

b='dynamic1'
D='10'
grammardir="/home/krish/codespace/experiment/grammars"

cmd="/usr/bin/timeout 10s python sinbad -b $b -d $D"
min1_cmd="${cmd} -m min1"
min4_cmd="${cmd} -m min4 -j /var/tmp/wrkdir/ambidexter/build/AmbiDexter.jar -T 30 -X 4G"

lang() {
  for l in Pascal SQL Java C; do
    for i in $(seq 5); do 
      min1td="/var/tmp/min1_${l}_${i}"
      min4td="/var/tmp/min4_${l}_${i}"
      rm -rf $min1td $min4td 
      cfg="${grammardir}/lang/acc/${l}.${i}.acc"
      lex="${grammardir}/lex/${l}.lex"
      $min1_cmd -x $min1td $cfg $lex > /dev/null 2>&1
      if [ -f $min1td/log ]; then
        finalmin1=$(tail -1 $min1td/log)
        _acc=$(echo $finalmin1 | cut -d, -f1)
        _lex=$(echo $finalmin1 | cut -d, -f2)
        $min4_cmd -x $min4td $_acc $_lex >/dev/null 2>&1
        from_min1=$(tail -1 $min1td/log | cut -d, -f5-7)
        from_min4=''
        [ -f $min4td/log ] && from_min4=$(tail -1 $min4td/log | cut -d, -f5-7)
        echo "$(head -1 $min1td/log | cut -d, -f1,5-7),,${from_min1},,${from_min4}"
      else
        echo "$cfg,,,"
      fi
    done
  done
}

bolz() {
  for g in $(seq 10 75); do
    for i in $(seq 10); do 
      min1td="/var/tmp/min1_${g}_${i}"
      min4td="/var/tmp/min4_${g}_${i}"
      rm -rf $min1td $min4td 
      mkdir -p $min1td $min4td 
      cfg="${grammardir}/boltzcfg/${g}/${i}.acc"
      lex="${grammardir}/boltzcfg/${g}/lex"
      $min1_cmd -x $min1td $cfg $lex > /dev/null 2>&1
      if [ -f $min1td/log ]; then
        finalmin1=$(tail -1 $min1td/log)
        _acc=$(echo $finalmin1 | cut -d, -f1)
        _lex=$(echo $finalmin1 | cut -d, -f2)
        $min4_cmd -x $min4td $_acc $_lex >${min4td}/min4.log 2>&1
        from_min1=$(tail -1 $min1td/log | cut -d, -f5-7)
        from_min4=''
        [ -f $min4td/log ] && from_min4=$(tail -1 $min4td/log | cut -d, -f5-7)
        echo "$(head -1 $min1td/log | cut -d, -f1,5-7),,${from_min1},,${from_min4}"
      else
        echo "$cfg,,,,"
      fi
    done
    rm -rf /tmp/tmp*
  done
}

mutlang() {
  for t in empty add; do # mutate delete switch; do 
    for l in Pascal SQL Java C CSS; do 
      for i in $(seq 1); do
        min1td="/var/tmp/min1_${t}_${l}_${i}"
        min4td="/var/tmp/min4_${t}_${l}_${i}"
        rm -rf $min1td $min4td 
        cfg="${grammardir}/mutlang/acc/$t/${l}/${l}.0_${i}.acc"
        lex="${grammardir}/lex/${l}.lex"
        $min1_cmd -x $min1td $cfg $lex > /dev/null 2>&1
        if [ -f $min1td/log ]; then
          finalmin1=$(tail -1 $min1td/log)
          _acc=$(echo $finalmin1 | cut -d, -f1)
          _lex=$(echo $finalmin1 | cut -d, -f2)
          $min4_cmd -x $min4td $_acc $_lex >/dev/null 2>&1
          from_min1=$(tail -1 $min1td/log | cut -d, -f5-7)
          from_min4=''
          [ -f $min4td/log ] && from_min4=$(tail -1 $min4td/log | cut -d, -f5-7)
          echo "$(head -1 $min1td/log | cut -d, -f1,5-7),,${from_min1},,${from_min4}"
        else
          echo "$cfg,,,"
        fi
      done
    done
  done
}

[ $cfgset == 'bolz' ] && bolz
[ $cfgset == 'lang' ] && lang
[ $cfgset == 'mutlang' ] && mutlang
