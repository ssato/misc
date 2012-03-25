#! /bin/bash
#
# Crop PDF
#
# Author: Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# Requirements: pdftk, pdftotext in poppler-utils (if title argument is not given).
#
set -e

usage="Usage: $0 INPUT_FILE OUTPUT_FILE [MARGIN]"


# Usage: get_cordinates INPUT_PDF
function get_cordinates () {
        sed -nre 's,.*MediaBox\s*\[([^]]+)\]/?.*,\1,p' "$1" | sort | uniq
}

# Usage: cat INPUT_PDF | crop MARGIN
function crop () {
        local margin=$1  # [%]

        local topleft=$2
        local topright=$3
        local bottomleft=$4
        local bottomright=$5

        topleft=$(echo "$topleft + $margin" | bc)
        topright=$(echo "$topright + $margin" | bc)
        bottomleft=$(echo "$bottomleft - $margin" | bc)
        bottomright=$(echo "$bottomright - $margin" | bc)

        sed -re "s,(Crop|Media)Box\s*\[([^]]+)\],\1Box\[$topleft $topright $bottomleft $bottomright\],g" | pdftk - output -
}

function mod_pdf () {
        local input="$1"
        local margin=$2

        local cordinates=`get_cordinates "$input"`
        local tl=`echo $cordinates | cut -f 1 -d ' '`
        local tr=`echo $cordinates | cut -f 2 -d ' '`
        local bl=`echo $cordinates | cut -f 3 -d ' '`
        local br=`echo $cordinates | cut -f 4 -d ' '`

        cat $input | crop $margin $tl $tr $bl $br
}


if test $# -lt 1; then
        echo $usage
        exit 1
fi

input="$1"
output="$2"
margin=$3

if test -z "$margin"; then margin=30; fi

if test "x$output" = "x$input" ; then
        echo "[Error] input $input equals to output $output."
        exit 1
fi

if test "$output" = "-"; then
        mod_pdf "$input" $margin
else
        mod_pdf "$input" $margin > $output
fi

