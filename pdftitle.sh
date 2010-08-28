#! /bin/bash
#
# Edit title of PDF file.
#
# Author: Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# Requirements: pdftk, pdftotext in poppler-utils (if title argument is not given).
#
set -e

usage="Usage: $0 INPUT_FILE OUTPUT_FILE [TITLE_NAME]"


# guess_title(input_file)
function guess_title () {
        pdftotext "$1" - | head -n 1
}

# Usage: cat INPUT_FILE | dump_metadata
function dump_metadata () {
        pdftk "$1" dump_data output -
}

# Usage: cat INPUT_FILE | dump_metadata | insert_title_in_metadata TITLE
function insert_title_in_metadata () {
        local title="$@"

        sed -e "1i \
InfoKey: Title\nInfoValue: $title"
}

# Usage: cat INPUT_FILE | dump_metadata | update_title_in_metadata TITLE
function update_title_in_metadata () {
        local org_title="$1"
        local title="$2"

        sed -e "s/InfoValue: $org_title/InfoValue: $title/"
}

# Usage: cat <metadata> | update_metadata INPUT_FILE
function update_metadata () {
        pdftk "$1" update_info - output -
}

function mod_pdf () {
        local input="$1"
        local title="$2"

        local org_title=$(pdfinfo $input | sed -nre "s/^Title: +(.+)$/\1/p")

        dump_metadata "$input" | insert_title_in_metadata "$title" | update_metadata "$input"
        #dump_metadata "$input" | update_title_in_metadata "$org_title" "$title" | update_metadata "$input"
}


if test $# -lt 1; then
        echo $usage
        exit 1
fi

input="$1"
output="$2"
title="$3"

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

mod_pdf "$input" "$title" > "$output"

