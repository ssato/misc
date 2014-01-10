#! /bin/bash
set -ex

srcdir=$(realpath ${0%/*})
conkydir=$HOME/.conky

if test -d $conkydir; then
    echo "$conkydir already exists!"
    exit 1
fi

(cd $HOME && ln -sf $srcdir .conky && ln -sf .conky/conkyrc .conkyrc)
