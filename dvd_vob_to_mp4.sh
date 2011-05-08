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

if test -z "$input"; then
    echo "Usage: $0 INPUT [OUTPUT]"
    exit 1
fi

output=$2
if test -z "$output"; then
    output=${input/.VOB/.mp4}
fi


# 1-pass: faster and smaller
#ffmpeg -i $input -f mp4 -vcodec libx264 -vpre default -acodec aac  -strict experimental $output

# 2-pass: much slower but can archive better quality
ffmpeg -i $input -y -pass 1 -an -vcodec libx264 -vpre slowfirstpass -vpre ipod640 \
        -b 1500kb -bt 1000kb -threads 0 -s 800x480 -aspect 16:9 -f ipod \
        $output
ffmpeg -i $input -y -pass 2 -vcodec libx264 -vpre hq -vpre ipod640 -b 1500kb \
        -bt 1000kb -threads 0 -s 800x480 -acodec aac  -strict experimental \
        -ab 192kb -ac 2 -aspect 16:9 -f ipod \
        $output

MP4Box -v -add $output -new $output.new 
