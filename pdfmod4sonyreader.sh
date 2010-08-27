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

# Usage: cat <metadata> | save_metadata INPUT_FILE OUTPUT_FILE
function save_metadata () {
        pdftk $1 update_info - output $2
}

function add_title () {
        local input=$1
        local output=$2

        shift 2
        local title="$@"

        dump_metadata $input | insert_title_in_metadata "$title" | save_metadata $input $output
}


if test $# -lt 2; then
        echo $usage
        exit 1
fi

input=$1
output=$2
title=$3
margin=$4   # Not implemented yet.

if test -z "$title"; then
        title=`guess_title $input`
fi

add_title $input $output "$title"
