#! /bin/sh

nosetests -c ${0%/*}/nose.cfg $@
