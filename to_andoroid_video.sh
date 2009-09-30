#! /bin/sh
#
# Optimize input MP4 file for Android.
#

set -e

input=$1
output=$2


if test $# -lt 2; then
  echo "Usage: $0 INPUT OUTPUT"
  exit 1
fi

# ffmpeg -i $input -s 480x320 -vcodec mpeg4 -acodec libfaac -ac 1 -ar 16000 -r 13 -ab 32000 -aspect 3:2 output-video.G1.mp4
ffmpeg -i $input -s 480x320 -vcodec mpeg4 -acodec libfaac -ac 1 -ar 16000 -r 13 -ab 32000 -aspect 3:2 $output
