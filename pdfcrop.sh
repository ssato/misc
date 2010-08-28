#! /bin/bash
#
# Optimize PDF file for Sony Reader.
#
# Author: Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# Requirements: pdftk, pdftotext in poppler-utils (if title argument is not given).
#
set -e

usage="Usage: $0 INPUT_FILE OUTPUT_FILE [TITLE_NAME] [MARGIN]"


# guess_title(input_file)
function guess_title () {
        pdftotext $1 - | head -n 1
}

# Usage: dump_metadata INPUT_FILE
function dump_metadata () {
        pdftk $1 dump_data output -
}

# Usage: dump_metadata | insert_title_in_metadata TITLE
function insert_title_in_metadata () {
        local title="$@"

        sed -e "1i \
InfoKey: Title\nInfoValue: $title"
}

# Usage: cat <metadata> | update_metadata INPUT_FILE
function update_metadata () {
        pdftk $1 update_info - output -
}

# Usage: get_cordinates INPUT_PDF
function get_cordinates () {
        sed -nre 's,.*MediaBox\s*\[([^]]+)\]/?.*,\1,p' $1 | sort | uniq
}

# Usage: cat INPUT_PDF | crop MARGIN
function crop () {
        local output=$1  # [%]
        local margin=$2

        local topleft=$3
        local topright=$4
        local bottomleft=$5
        local bottomright=$6

        #topleft=$(echo "$topleft + $topleft * $margin / 100" | bc)
        #topright=$(echo "$topright + $topright * $margin / 100" | bc)
        #bottomleft=$(echo "$bottomleft - $bottomleft * $margin / 100" | bc)
        #bottomright=$(echo "$bottomright - $bottomright * $margin / 100" | bc)

        topleft=$(echo "$topleft + $margin" | bc)
        topright=$(echo "$topright + $margin" | bc)
        bottomleft=$(echo "$bottomleft - $margin" | bc)
        bottomright=$(echo "$bottomright - $margin" | bc)

        sed -nre "s,(Crop|Media)Box\s*\[([^]]+)\],\1Box\[$topleft $topright $bottomleft $bottomright\],g" | pdftk - output $output
}

function mod_pdf () {
        local input=$1
        local output=$2
        local title="$3"
        local margin=$4

        local cordinates=`get_cordinates $input`
        local tl=`echo $cordinates | cut -f 1 -d ' '`
        local tr=`echo $cordinates | cut -f 2 -d ' '`
        local bl=`echo $cordinates | cut -f 3 -d ' '`
        local br=`echo $cordinates | cut -f 4 -d ' '`

        #dump_metadata $input | insert_title_in_metadata "$title" | update_metadata $input | crop $output $margin $tl $tr $bl $br 
        dump_metadata $input | insert_title_in_metadata "$title" | update_metadata $input > $output
}


if test $# -lt 2; then
        echo $usage
        exit 1
fi

input=$1
output=$2
title="$3"
margin=$4

if test "x$output" = "x$input" ; then
        echo "[Error] input $input equals to output $output."
        exit 1
fi

if test -z "$title"; then
        title=`guess_title $input`
        if test -z "$title"; then
                echo "[Error] Could not get the appropriate title for $input"
                exit 1
        fi
fi

if test -z "$margin"; then
        margin=20
fi


mod_pdf $input $output "$title" $margin
