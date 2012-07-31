#! /bin/sh

# We assume the following programs/tools exist:
# wget, git, bunzip2, Python 2.7, Java


missing=0
check_for () {
	which $1 > /dev/null 2> /dev/null
    if [ $? -ne 0 ]; then
        echo "Error: can't find $1 binary"
        missing=1
    fi
}

check_for git
check_for wget
check_for bunzip2
which pypy > /dev/null 2> /dev/null
if [ $? -eq 0 ]; then
    PYTHON=`which pypy`
else
    check_for python
    PYTHON=`which python`
fi
check_for java
check_for javac
which gmake > /dev/null 2> /dev/null
if [ $? -eq 0 ]; then
    MYMAKE=gmake
else
    MYMAKE=make
fi

if [ $missing -eq 1 ]; then
    exit 1
fi

java -version 2>&1 | tail -n 1 | grep "OpenJDK .*Server VM (build [a-zA-Z0-9.\-]*, mixed mode)" > /dev/null 2> /dev/null
if [ $? -ne 0 ]; then
    cat << EOF
Warning: incorrect version of Java detected. Expected:
  OpenJDK Server VM (build ..., mixed mode)
You should download the correct version and put it in your PATH.
EOF
    echo -n "Continue building anyway? [Ny] "
    read answer
    case "$answer" in
        y | Y) ;;
        *) exit 1;;
    esac
fi

python -V 2>&1 | egrep -o '[0-9].[0-9]' > /dev/null 2> /dev/null
if [ $? -ne 0 ]; then
    cat << EOF
Warning: incorrect version of Python detected. Expected:
  Python 2.7 or above
You should download the correct version and put it in your PATH.
EOF
    echo -n "Continue building anyway? [Ny] "
    read answer
    case "$answer" in
        y | Y) ;;
        *) exit 1;;
    esac
fi

if [ $# -eq 0 ]; then
    wrkdir=`pwd`
elif [ $# -eq 1 ]; then
    wrkdir=$1
    mkdir -p $wrkdir
else
    echo "$0 [<full path to working directory>]"
    exit 1
fi
echo "===> Working in $wrkdir"

# Download SinBAD

echo "\\n===> Fetching SinBAD tool\\n"

cd $wrkdir
git clone git@github.com:nvasudevan/sinbad.git
cd sinbad
git checkout 8f99f2d111
cd $wrkdir

# Download ACLA

echo "\\n===> Fetching ACLA tool\\n"

cd $wrkdir
mkdir ACLA
cd ACLA
wget http://www.brics.dk/grammar/dist/grammar-all.jar

# Download AmbiDexter

echo "\\n===> Fetching AmbiDexter tool\\n"

cd $wrkdir
git clone git://github.com/cwi-swat/ambidexter.git
cd ambidexter
git checkout db64485ad4
mkdir -p build/META-INF
echo "Main-Class: nl.cwi.sen1.AmbiDexter.Main" > build/META-INF/MANIFEST.MF
patch -b -R -p0 src/nl/cwi/sen1/AmbiDexter/derivgen/ParallelDerivationGenerator.java < $wrkdir/sinbad/experiment/patches/AmbiDexter.patch || exit $?
cd src
javac nl/cwi/sen1/AmbiDexter/*.java || exit $?
find . -type f -name "*.class" | cpio -pdm ../build/
cd ../build
jar cmf META-INF/MANIFEST.MF AmbiDexter.jar nl





