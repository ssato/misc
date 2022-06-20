FROM fedora/systemd-systemd:latest
MAINTAINER Satoru SATOH <satoru.satoh@gmail.com>
RUN dnf update -y && \
    dnf install --allowerasing -y gcc git python3 python3-libselinux python3-devel sudo && \
    ln -s /usr/bin/python3 /usr/bin/python

ENV SHELL /bin/bash
