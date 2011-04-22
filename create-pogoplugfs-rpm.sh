#! /bin/bash
# Build SRPM from pogopluginstall archive.
# 
# Author: Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
# Requirements: pmaker in packagemaker available from
#               https://github.com/ssato/rpmkit/
#
set -e

archive=$1
#arch=$(uname -m)

if test "x$archive" = "x"; then
    echo "Usage: $0 POGOPLUGINSTALL_ARCHIVE_FILE"
    exit 1
fi

requires="fuse-libs"


workdir=$(mktemp -d --suffix=pogoplug)
bindir=$workdir/usr/bin

mkdir -p $bindir
tar zxvf $archive -C $bindir

version=$($bindir/pogoplugfs --version | sed 's,LINUX GENERIC - ,,g')


echo $bindir/pogoplugfs | \
pmaker -n pogoplugfs \
       --license Commercial \
       --group "System Environment/Libraries" \
       --pversion $version \
       --url http://my.pogoplug.com \
       --summary "Pogoplug client tool" \
       --relations "requires:$requires" \
       --arch \
       --upto build \
       -w $workdir --destdir $workdir \
       --ignore-owner -


# vim: set sw=4 ts=4 et:
