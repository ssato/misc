#! /bin/bash
#
# build srpm in current dir or specified working dir from given rpm spec.
#
# Author: Satoru SATOH <ssato redhat.com>
# License: MIT
#
# Requirements: rpm-python, rpm-build
#

function get_source0 () {
    python -c "import rpm; import sys; print rpm.spec('$1').sources[0][0]"
}

function get_url () {
    python -c "import rpm; import sys; print rpm.spec('$1').sourceHeader['URL']"
}


if test -z "$1"; then
    echo "Usage: $0 RPM_SPEC [WORKDIR]"
    exit 0
fi
rpmspec=$1
workdir=$2

if test -z "$workdir"; then
    workdir=`pwd`
fi

src0_url=$(get_source0 $rpmspec)
src0=$(basename $src0_url)

if test -f $workdir/$src0; then
    echo "[Info] Found the source: $src0"
else
    # TODO: How to get the source0's URL ?
    if test ! `echo $src0_url | grep -E '^(http|ftp)' 2>&1 > /dev/null`; then
        src0_url=`get_url $rpmspec`"$src0"
    fi
fi

test -f $workdir/$src0 || curl --insecure --location -o $workdir/$src0 $src0_url

rpmbuild --define "_srcrpmdir $workdir" --define "_sourcedir $workdir" --define "_buildroot $workdir" -bs $rpmspec
