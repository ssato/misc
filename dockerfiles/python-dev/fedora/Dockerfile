# The latest stable release of Fedora:
FROM fedora:23
MAINTAINER https://github.com/ssato/misc/dockerfiles/python-dev

RUN dnf -y update && dnf install -y findutils which gcc make git tar zip yum pylint python3-pylint python{,3}-{pip,flake8,nose,pep8,docopt,coverage,requests,devel,setuptools,tools} python-tox && dnf clean all
RUN pip install coveralls
