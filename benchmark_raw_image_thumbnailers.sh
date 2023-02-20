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

# TODO: exiv2 (no output option)
declare -a thumbnailers=(
    "rawtherapee-cli -n -Y -f -o OUTPUT -c INPUT"
    "raw-thumbnailer -s 128 INPUT OUTPUT"
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
        cmd_fmt="${thumbnailers[$i]}"
	echo "## ${cmd_fmt}"
        time {
            for f in $files; do
                bfn=${f##*/}
                bfn_wo_ext=${bfn%.*}
                out=${outdir}/${bfn_wo_ext}${suffix}
                cmd="${cmd_fmt/INPUT/${f}}"; cmd="${cmd/OUTPUT/${out}}"
                eval "${cmd} 2>&1 > ${out}.log"
		echo -ne "."
            done
        }
	echo ""
    done
}

[[ $# -gt 0 ]] && benchmark $@
