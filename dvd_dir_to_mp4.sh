#! /bin/sh
#
# Encode DVD Dir to MP4 file
#

set -e


input=$1
output=$2
chapter=$3

if test $# -lt 2; then
  echo "Usage: $0 DVD_DIR OUTPUT [CHAPTER]"
  exit 1
fi

if test $# -eq 2; then
  chapter=1
fi


mencoder -dvd-device $input dvd://$chapter \
  -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=800:vhq \
  -oac mp3lame -lameopts abr:br=128:q=9:vol=10 \
  -ffourcc DIVX -o $output

