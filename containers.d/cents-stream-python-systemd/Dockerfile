FROM quay.io/centos/centos:stream8
MAINTAINER Satoru SATOH <satoru.satoh@gmail.com>
ENV container docker

RUN dnf -y update && dnf clean all
RUN dnf -y install systemd && dnf clean all && \
(cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;

RUN dnf install --allowerasing -y gcc git python3 python3-libselinux python3-devel sudo && \
    ln -s /usr/bin/python3 /usr/bin/python

VOLUME [ "/sys/fs/cgroup", "/tmp", "/run" ]

ENV SHELL /bin/bash
CMD ["/sbin/init"]
