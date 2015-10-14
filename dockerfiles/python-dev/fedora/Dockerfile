# The latest stable release of Fedora:
FROM fedora:22
MAINTAINER https://github.com/ssato/misc/dockerfiles/python-dev

RUN dnf -y update && dnf clean all

RUN dnf install -y findutils gcc make git tar zip yum pylint python3-pylint python{,3}-{pip,flake8,nose,pep8,docopt,coverage,requests,devel,setuptools,tools} python-tox
RUN pip install coveralls
