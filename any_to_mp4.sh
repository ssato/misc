#! /bin/bash
#
# Create mp4 (h.264) video from VOB (DVD Movie) file with using ffmpeg
#
# Author: Satoru SATOH <satoru.satoh at gmail.com>
# License: MIT
#
# Requirements: ffmpeg and MP4Box (rpm: gpac)
#

set -e

input=$1
output=$2

if test -z "$input"; then
    echo "Usage: $0 INPUT [OUTPUT]"
    exit 1
fi

if test -z "$output"; then
    output=$input.mp4
fi


# 2-pass: slower but can archive better quality
ffmpeg -i $input -y -pass 1 -an -vcodec libx264 -vpre slowfirstpass -vpre ipod640 \
        -b 1500kb -bt 1000kb -threads 0 -s 800x480 -aspect 16:9 -f ipod \
        $output

ffmpeg -i $input -y -pass 2 -vcodec libx264 -vpre hq -vpre ipod640 \
        -b 1500kb -bt 1000kb -threads 0 -s 800x480 -aspect 16:9 -f ipod \
        -strict experimental -ab 192kb -ac 2 -acodec aac \
        $output

MP4Box -v -add $output -new $output.new
cp -f $output.new $output
