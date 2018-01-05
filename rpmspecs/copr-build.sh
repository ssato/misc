#! /bin/bash
# Build SRPM and submit new build to copr.
#
# References:
# - https://developer.fedoraproject.org/deployment/copr/copr-cli.html
# - http://copr-rest-api.readthedocs.io/en/latest/Resources/build.html#submit-new-build
#
set -ex

copr_project=ssato/python-anyconfig

curdir=${0%/*}
topdir=${curdir}/../
srpm=$1

if test "x${srpm}" = "x"; then
    echo "Usage: $0 SRPM_PATH"
    exit -1
fi

test -f ~/.config/copr
copr-cli build ${copr_project:?} ${srpm:?}

# vim:sw=4:ts=4:et:
