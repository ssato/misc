#! /bin/bash
# A tiny script to extract contents from an ISO9660 image.
#
# Author: Satoru SATOH <ssato@redhat.com>
# License: BSD style
#
set -e

isoexts=
isoimg=


# options:
outdir=out
target=
verbose=0
isoinfo="/usr/bin/isoinfo"


usage="Usage: $0 [OPTIONS] ISO_IMAGE"

function show_help () {
  cat <<EOH
$usage
Options:
  -d DIR    Directory to dump files. [Default: out/]
  -f FILE   Specify a file in full path (in iso image) to extract.
            [Default: all files]
  -x PATH   Specify the path to isoinfo.

  -h        Show this help and exit.
  -v        Verbose mode.

Examples:
 $0 -d outdir/ foo.iso 
 $0 -v -f /path/to/README.txt bar.iso 
EOH
}


while getopts "d:f:x:hv" opt
do
  case $opt in
    d) outdir=$OPTARG ;;
    f) target=$OPTARG ;;
    x) isoinfo=$OPTARG ;;
    v) verbose=1 ;;
    h) show_help; exit 0 ;;
    \?) show_help; exit 1 ;;
  esac
done
shift $(($OPTIND - 1))


function vecho () {
  (test "x$verbose" = "x1" && echo $@ || echo -ne "" )
}


if test $# -lt 1; then
  echo "$usage"
  exit 1
fi

isoimg=$1


if test ! -x $isoinfo; then
  cat <<EOM
[Fatal] isoinfo is not found in your \$PATH

$0 needs isoinfo from genisoimage or cdrecord.
Please install any of them first.
EOM
  exit 1
fi

if test ! -f $isoimg; then
  echo "[Error] ISO Image '$isoimg' is not found."
  exit 1
fi

if test -z $target; then
  if test ! -d $outdir; then
    vecho "[Info] Directory '$outdir' is not found. Create it."
    mkdir -p $outdir
  fi
fi


# Detect extensions used.
info=$($isoinfo -d -i $isoimg)
(echo $info | grep 'NO Joliet present' > /dev/null 2>&1) || isoexts="-J"
(echo $info | grep 'NO Rock Ridge present' > /dev/null 2>&1) || isoexts="$isoexts -R"


if test -z $target; then
  files=$($isoinfo $isoexts -i $isoimg -f)
  dirs=$(for f in $files; do echo $outdir${f%/*}; done | uniq)

  mkdir -p $dirs

  for f in $files; do
    ($isoinfo $isoexts -i $isoimg -x $f > $outdir$f \
      || vecho "[Info] Not a file. Skipped: $f") 2> /dev/null 
  done
else
  $isoinfo $isoexts -i $isoimg -x $target  > ${target##*/}
fi

exit $?
