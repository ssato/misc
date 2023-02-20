#! /bin/bash
# SPDX-License-Identifier: MIT
# Copyright(C) 2023 Satoru SATOH
#
# Benchmark script for some RAW image thumbnailers.
#
set -e -o pipefail

curdir=${0%/*}
outdir=${curdir}/out
suffix="-thumb.png"

# seealso: https://support.system76.com/articles/fix-raw-image-previews/
function rawtherapee_cli () {
    rawtherapee-cli -n -Y -f -c $1 -o $2
}

# seealso: `raw-thumbnailer -h`
function raw_thumbnailer () {
    raw-thumbnailer -s 128 $1 $2
}

#
# todo: exiv2; It has no any options to specify output file path, AFAIK.
# function exiv2 () { ... }

declare -a thumbnailers=(
    "rawtherapee_cli"
    "raw_thumbnailer"
)

usage="
Usage: $0 FILES...
Options:
  -o OUTPUT_DIR  Specify a path to dir to output generated thumbnail files.
                 [${curdir:?}/out/]
  -s SUFFIX      Specify the suffix of output thumbnail files.
                 [${suffix:?}]
"

while getopts o:s: OPT
do
    case $OPT in
      "o") outdir=${OPTARG};;
      "s") suffix=${OPTARG};;
      *) echo "${usage}";;
     esac
done
shift $((${OPTIND} - 1))

function benchmark () {
    local files=$@

    mkdir -p ${outdir}

    for i in ${!thumbnailers[@]}; do
	thumbnailer_fn="${thumbnailers[$i]}"
	echo -n "${thumbnailer_fn/_/-}: "
        time {
            for f in $files; do
                bfn=${f##*/}
                bfn_wo_ext=${bfn%.*}
                out=${outdir}/${bfn_wo_ext}${suffix}
                eval "${thumbnailer_fn} $f $out 2>&1 > ${out}.log"
		echo -n "."
            done
        }
	echo ""
    done
}

[[ $# -gt 0 ]] && benchmark $@ || { echo "$usage"; exit 1; }
