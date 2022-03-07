#! /bin/bash
#
# Extract specific data from https://www.mizuhobank.co.jp/market/historical.html
#
set -ex -o pipefail

sed -r '
1d
s/^([^,]+,[^,]+),.*/\1/
' $1

# vim:sw=4:ts=4:et
