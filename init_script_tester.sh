#!/bin/bash
#
# Init script test tool.
#
# Copyright (C) 2014 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: MIT
#
# How to test your init script:
#   1. Stop your application with your init script before running tests.
#   2. Run this script with specifing the path to your init script like this:
#
#        # ./init_script_tester.sh [Options...] /path/to/your/init_script
#
# Here is an example session log:
#
# ssato@localhost% ./init_script_tester.sh \
# > -E "PIDFILE=/tmp/t.pid LOCKFILE=/tmp/t.lock" \
# > -T "rm -f /tmp/t.pid" \
# > ./init_script_example.sh
# [Info] Prepare to test './init_script_example.sh' (make sure it's stopped)...  Done
#   Check if to start from stopped state exits with exit code 0 ...       OK
#   Check if to start from started state exits with exit code 0 ...       OK
#   Check if to restart from started state exits with exit code 0 ...     OK
#   Check if 'status' after started exits with exit code 0 ...    OK
#   Check if to stop from started state exits with exit code 0 ...        OK
#   Check if 'status' after stopped exits with exit code 3 ...    OK
#   Check if to stop from stopped state exits with exit code 0 ...        OK
#   Check if to restart from stopped state exits with exit code 0 ...     OK
#   Check if to stop from restared state exits with exit code 0 ...       OK
# [Info] Prepare to test force-stop from abnormal state...        Done
#   Check if to force-stop from abnormal state exits with exit code 0 ... OK
# ssato@localhost%
#
USAGE="Usage: $0 [Options...] /path/to/your/init_script"

function show_help () {
    cat <<EOH
${USAGE}
Options:
    -E ENV_STRINGS    Environment variable definitions will be passed to your
                      init script, ex. -E "LANG=C PIDFILE=/tmp/t.pid".
    -T TROUBLEMAKER   Command to put services in abnormal state on purpose, to
                      test force-stop from abnormal state works fine if needed.

                      You can use shell functions defined in
                      /etc/rc.d/init.d/functions in this,
                      ex. -T "killproc -p /var/run/foo.pid foo".
EOH
}

function test_helper () {
    local expected_rc=$1
    local test_desc="$2"
    local test_body="$3"

    echo -ne "  Check if ${test_desc:?} exits with exit code ${expected_rc:?} ...\t"
    eval "${test_body:?} >/dev/null"; rc=$?
    if test $rc -ne ${expected_rc}; then
        echo "Failed. rc=$rc"
        exit -1
    else
        echo "OK"
    fi
}

run_troublemaker () {
    local target=$1
    local test_env="$2"
    local troublemaker="$3"

    echo -ne "[Info] Prepare to test force-stop certainly from abnormal state...\t"
    eval "${test_env:?} ${target} status >/dev/null"; rc=$?
    if test $rc -eq 0; then  # It's running.
        :  # Nothing to do.
    elif test $rc -eq 3; then  # It's stopped.
        eval "${test_env} ${target} start >/dev/null"; rc=$?
        if test $rc -ne 0; then
            echo "NG; failed to start ${target}."
            exit 1
        fi
    else
        echo "NG; unknown state"
        exit 1
    fi
    eval "${troublemaker:?}"; rc=$?
    if test $rc -ne 0; then
        echo "NG; failed to put ${target} into abnormal state."
        exit 1
    fi
    echo "Done"
    test_helper 0 "to force-stop certainly from abnormal state" "${test_env} ${target} stop"
}

# see also: http://refspecs.linuxfoundation.org/LSB_4.1.0/LSB-Core-generic/LSB-Core-generic/iniscrptact.html
run_testcases () {
    local target=$1
    local test_env="$2"
    local troublemaker="$3"

    echo -ne "[Info] Prepare to test '${target:?}' (make sure it's stopped)...\t"
    eval "${test_env} ${target} status"; rc=$?
    if test $rc -ne 3; then
        echo "${target} is not stopped or '${target} status' exited w/ wrong exit code. Aborting tests..."
        exit -1
    fi
    echo "Done"

    test_helper 0 "to start from stopped state" "${test_env} ${target} start"
    test_helper 0 "to start from started state" "${test_env} ${target} start"
    test_helper 0 "to restart from started state" "${test_env} ${target} restart"
    test_helper 0 "'status' after started" "${test_env} ${target} status"
    test_helper 0 "to stop from started state" "${test_env} ${target} stop"
    test_helper 3 "'status' after stopped" "${test_env} ${target} status"
    test_helper 0 "to stop from stopped state" "${test_env} ${target} stop"
    test_helper 0 "to restart from stopped state" "${test_env} ${target} restart"
    test_helper 0 "to stop from restared state" "${test_env} ${target} stop"

    # Special cases:
    if test "x$troublemaker" != "x"; then
        run_troublemaker ${target} "${test_env}" "${troublemaker}"
    fi
}

source /etc/rc.d/init.d/functions

ENV=
TROUBLEMAKER=
while getopts "E:T:h" opt
do
  case $opt in
    E) ENV="$OPTARG" ;;
    T) TROUBLEMAKER="$OPTARG" ;;
    h) show_help; exit 0 ;;
    \?) show_help; exit 1 ;;
  esac
done
shift $(($OPTIND - 1))

TARGET_INIT_SCRIPT=$1
if test "x${TARGET_INIT_SCRIPT}" = "x"; then
    echo "${USAGE}"
    exit 0
fi

run_testcases $TARGET_INIT_SCRIPT "$ENV" "$TROUBLEMAKER"
exit $?

# vim:sw=4:ts=4:et:
