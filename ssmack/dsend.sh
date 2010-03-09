#! /bin/sh
# 
# Copyed from http://wiki.beryl-project.org/wiki/Tips/DBUS_HowTo
set -e

dbus_send="/bin/dbus-send"
xwininfo="/usr/bin/xwininfo"

if test ! -x ${dbus_send:?}; then
        echo "Not found: ${dbus_send}"
        exit 1
fi
if test ! -x ${xwininfo:?}; then
        echo "Not found: ${xwininfo}"
        exit 1
fi

xinfo="${xwininfo:?} -root | grep id: | awk '{ print $4 }'"

${dbus_send:?} --type=method_call --dest=org.freedesktop.beryl \
        /org/freedesktop/beryl/$1/allscreens/$2 org.freedesktop.beryl.activate \
        string:'root' \
        int32:$(${xwininfo:?} -root | grep id: | awk '{ print $4 }') \
        $3 $4 $5 $6 $7 $8 $9 

exit $?
