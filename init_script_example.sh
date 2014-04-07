#!/bin/bash
#
# Init script script example.
#
# Copyright (C) 2014 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: MIT
#
# Install:
#   1. Modify this script to fit with your application or something and your
#      purpose. Do not forget test it with init_script_tester.sh.
#
#   2. Install it in /etc/rc.d/init.d/ with appropriate attributes (permission,
#      owner, group and SELinux label, etc.) and name represents the
#      application or something you want to control with this script like the
#      followings:
#       
#      # install -m 755 <this script> /etc/rc.d/init.d/<application_name>
#      # restorecon -rv /etc/rc.d/init.d/
#
# chkconfig: - 85 15
# description: Init script example
# processname: <enter_your_app_process_etc>
# config: /etc/sysconfig/<enter_your_app_name_etc>
# pidfile: /var/run/<enter_your_app_name_etc>.pid
#
### BEGIN INIT INFO
# Provides: <enter_your_app_name_etc>
# Required-Start: $local_fs $remote_fs $network $named
# Required-Stop: $local_fs $remote_fs $network
# Short-Description: Init script example
# Description: Init script example with tests
### END INIT INFO

# Example session log:
#
# ssato@localhost% ln -s init_script_example.sh foo
# ssato@localhost% PIDFILE=/tmp/foo.pid LOCKFILE=/tmp/foo.lock ./foo; echo $?
# Usage: foo {start|stop|status|restart|condrestart|try-restart
# 2
# ssato@localhost% PIDFILE=/tmp/foo.pid LOCKFILE=/tmp/foo.lock ./foo start; echo $?
# Starting foo: 
# 0
# ssato@localhost% PIDFILE=/tmp/foo.pid LOCKFILE=/tmp/foo.lock ./foo status; echo $?
# 0
# ssato@localhost% PIDFILE=/tmp/foo.pid LOCKFILE=/tmp/foo.lock ./foo stop; echo $?
# Stopping foo: 
# 0
# ssato@localhost% PIDFILE=/tmp/foo.pid LOCKFILE=/tmp/foo.lock ./foo status; echo $?
# 3
#

# Edit and customize this:
#MY_APP_NAME=foo
MY_APP_NAME=${0##*/}

. /etc/rc.d/init.d/functions
test -f /etc/sysconfig/${MY_APP_NAME} && . /etc/sysconfig/${MY_APP_NAME}

# Start it in the C locale by default.
MY_APP_LANG=${MY_APP_LANG-"C"}

prog=${MY_APP_NAME}  # e.g. /usr/sbin/httpd
pidfile=${PIDFILE-/var/run/${MY_APP_NAME}.pid}
lockfile=${LOCKFILE-/var/lock/subsys/${MY_APP_NAME}}
STOP_TIMEOUT=${STOP_TIMEOUT-10}

start () {
    echo -n $"Starting $prog: "
    # There is no '${MY_APP_NAME}' daemon exists in actual as this script is
    # just an example so the line below must be commented:
    #LANG=$MY_APP_LANG daemon --pidfile=${pidfile} ${prog} $OPTIONS
    LANG=$MY_APP_LANG touch ${pidfile}  # Just create empty PID file instead.
    local rc=$?
    echo
    [ $rc = 0 ] && touch ${lockfile}
    return $rc
}

# When stopping MY_APP_NAME, a delay (of default 10 second) is required before
# SIGKILLing the MY_APP_NAME parent; this gives enough time for the MY_APP_NAME parent to
# SIGKILL any errant children.
stop() {
	echo -n $"Stopping $prog: "
	# Likewise. See the comment in 'start' shell function also.
	#killproc -p ${pidfile} -d ${STOP_TIMEOUT} $MY_APP_NAME
	local rc=$?
	echo
	[ $rc = 0 ] && rm -f ${lockfile} ${pidfile}
}

my_status () {
    #status -p ${pidfile} $MY_APP_NAME; rc=$?
    # if test $rc -eq 0; then
    test -f ${lockfile} && return 0 || return 3
    # else
    #     exit 1
    # fi
}

case "$1" in
  start)
        my_status; rc=$?
        if test $rc -eq 3; then  # It's stopped.
            start; rc=$?
        fi
        ;;
  stop)
        my_status; rc=$?
        if test $rc -eq 0; then  # It's running.
            stop; rc=$?
        else
            rc=0
        fi
        ;;
  status)
        my_status; rc=$?
        ;;
  restart)
        my_status; rc=$?
        if test $rc -eq 3; then
            start; rc=$?
        elif test $rc -eq 0; then
            stop && start; rc=$?
        fi
        ;;
  condrestart|try-restart)
        my_status; rc=$?
        if test $rc -eq 0; then
            stop && start; rc=$?
        else
            rc=0
        fi
        ;;
  *)
        echo $"Usage: $prog (start|stop|status|restart|condrestart|try-restart)"
        rc=1
esac
exit $rc

# vim:sw=4:ts=4:et:
