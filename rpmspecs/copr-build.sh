#! /bin/bash
# Build SRPM and submit new build to copr.
#
# References:
# - https://developer.fedoraproject.org/deployment/copr/copr-cli.html
# - http://copr-rest-api.readthedocs.io/en/latest/Resources/build.html#submit-new-build
#
set -e

curdir=${0%/*}
topdir=${curdir}/../
srpm=$1
copr_project=${2:-ssato/python-anyconfig}

if test "x${srpm}" = "x"; then
    echo "Usage: $0 SRPM_PATH [COPR_PROJECT]"
    exit -1
fi

set -x
test -f ~/.config/copr
copr-cli build ${copr_project:?} ${srpm:?}

# vim:sw=4:ts=4:et:
