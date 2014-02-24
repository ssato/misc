#!/bin/bash
#
# Init script script tester.
#
# Copyright (C) 2014 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: MIT
#
# How to test your init script:
#   1. Stop your application before tests.
#   2. Run this script with specifing your init script like this:
#        # ./init_script_tester.sh /path/to/your/init_script    
#
# Example session log:
#
# ssato@localhost% ./init_script_tester.sh -E "PIDFILE=/tmp/t.pid LOCKFILE=/tmp/t.lock" ./init_script_example.sh
# Make sure that './init_script_example.sh' is stopped ...        OK
# Check if to start from stopped state exits with exit code 0 ... OK
# Check if to start from started state exits with exit code 0 ... OK
# Check if to restart from started state exits with exit code 0 ...       OK
# Check if 'status' on started state exits with exit code 0 ...   OK
# Check if to stop from started state exits with exit code 0 ...  OK
# Check if 'status' on stopped state exits with exit code 3 ...   OK
# Check if to stop from stopped state exits with exit code 0 ...  OK
# Check if to restart from stopped state exits with exit code 0 ...       OK
# Check if to stop from restared state exits with exit code 0 ... OK
# ssato@localhost%
# 
USAGE="Usage: $0 [Options...] /path/to/your/init_script"

function show_help () {
    cat <<EOH
${USAGE}
Options:
    -E ENV_STRINGS   Environment variable definitions will be passed to your
                     init script, ex. -E "LANG=C PIDFILE=/tmp/t.pid".
EOH
}

function test_helper () {
    local expected_rc=$1
    local test_desc="$2"
    local test_body="$3"

    echo -ne "Check if ${test_desc:?} exits with exit code ${expected_rc:?} ...\t"
    eval "${test_body:?} >/dev/null"; rc=$?
    if test $rc -ne ${expected_rc}; then
        echo "Failed. rc=$rc"
        exit -1
    else
        echo "OK"
    fi
}

# see also: http://refspecs.linuxbase.org/LSB_3.1.1/LSB-Core-generic/LSB-Core-generic/iniscrptact.html
run_testcases () {
    local target=$1; shift
    local test_env="$@"

    echo -ne "Make sure that '${target:?}' is stopped ...\t"
    eval "${test_env} ${target} status"; rc=$?
    if test $rc -ne 3; then
        echo "${target} is not stopped or '${target} status' exited w/ wrong exit code. Aborting tests..."
        exit -1
    fi
    echo "OK"

    test_helper 0 "to start from stopped state" "${test_env} ${target} start"
    test_helper 0 "to start from started state" "${test_env} ${target} start"
    test_helper 0 "to restart from started state" "${test_env} ${target} restart"
    test_helper 0 "'status' on started state" "${test_env} ${target} status"
    test_helper 0 "to stop from started state" "${test_env} ${target} stop"
    test_helper 3 "'status' on stopped state" "${test_env} ${target} status"
    test_helper 0 "to stop from stopped state" "${test_env} ${target} stop"
    test_helper 0 "to restart from stopped state" "${test_env} ${target} restart"
    test_helper 0 "to stop from restared state" "${test_env} ${target} stop"
}

ENV=
while getopts "E:h" opt
do
  case $opt in
    E) ENV="$OPTARG" ;;
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

run_testcases $TARGET_INIT_SCRIPT $ENV
exit $?

# vim:sw=4:ts=4:et:
