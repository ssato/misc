#! /bin/bash
# Build SRPM from flash plugin for linux x86_64 archive.
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
    echo "Usage: $0 ARCHIVE_FILE"
    exit 1
fi


requires="mozilla-filesystem"
version=$(echo $archive | sed -r "s,.*flashplayer([0-9]+)_([0-9]+)_([^_]+)_64bit_linux_([^.]+).tar.gz,\1.\2.\3.\4,")
target=libflashplayer.so


workdir=$(mktemp -d --suffix=flashplugin-)
tar zxvf $archive -C $workdir
chmod +x $workdir/$target

echo $workdir/$target,target=/usr/lib64/mozilla/plugins/libflashplayer.so | \
pmaker -n flash-plugin \
       --license Commercial \
       --group "Applications/Internet" \
       --pversion $version \
       --url http://labs.adobe.com/downloads/flashplayer10_square.html \
       --summary "Adobe Flash Player Preview Release for linux x86_64" \
       --relations "requires:$requires" \
       --itype filelist.ext \
       --arch \
       --upto build \
       --no-mock --no-rpmdb \
       -w $workdir --destdir $workdir \
       --ignore-owner -


# vim: set sw=4 ts=4 et:
