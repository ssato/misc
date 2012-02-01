#! /bin/bash

if test -z "$1"; then
    echo "Usage: $0 RPM_SPEC [WORKDIR]"
    exit 0
fi
rpmspec=$1
workdir=$2

if test -z "$workdir"; then
    workdir=`pwd`
fi


rpmbuild --define "_srcrpmdir $workdir" --define "_sourcedir $workdir" --define "_buildroot $workdir" -bs $rpmspec
