#! /bin/bash
# Quick hack to generate kickstart file from RPM DB of which root was given.
#
# Author: Satoru SATOH <ssato at redhat.com>
# License: MIT
# Requirements: pwgen, http://sf.net/projects/pwgen
#
set -e

root=${2:-/}
password=${3:-$(pwgen -cn0sB -1)}

function usage () {
    cat << EOU
$0 OUTPUT [RPM_ROOT [PASSWORD]]
where OUTDIR    Dir to save outputs
      RPM_ROOT  Abosolute path of the root in which var/lib/rpm exists [$root]
      PASSWORD  Root password of root of the host to build by this ks.cfg [${password}]
                generated
EOU
}

function rpms_by_name () {
    rpm --qf '%{n}\n' -qa --define "_topdir ${root}" | sort | uniq
}

outdir=${1}
if test "x${outdir}" = "x"; then
    usage; exit 0
fi

echo "[Info] Collect RPM names from ${root} ..."
kscfg="
install
cdrom
text
bootloader
keyboard us
lang en_US.UTF-8
rootpw ${password}
timezone Asia/Tokyo --utc
selinux --enforcing
skipx
authconfig --enableshadow --passalgo=sha512
firewall --enabled --ssh
services --enabled iptables,ntpd,ntpdate,sshd --disabled ip6tables,lvm2-monitor,lvm2-lvmetad,mdmonitor
network --device=eth0 --onboot=yes --bootproto=dhcp
zerombr
clearpart --all --initlabel
autopart
reboot

%packages --ignoremissing
$(rpms_by_name)
%end

%pre
%end

%post --nochroot
test -d /mnt/sysimage/root/setup || mkdir -p /mnt/sysimage/root/setup
test -f /tmp/boot-params && cp -f /tmp/boot-params /mnt/sysimage/root/setup
%end

%post
set -x -v
exec 1>/root/setup/kickstart.post.log 2>&1
test -f /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release && \
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release || :

touch /root/setup/kickstart.post.stamp
%end
"

mkdir -p ${outdir}

echo "[Info] Genrating ks.cfg and vmbuild.sh for ${root} in ${outdir} ..."
cat << EOK > ${outdir}/ks.cfg
${kscfg}
EOK

cat << 'EOV' > ${outdir}/vmbuild.sh
#! /bin/bash
# see also virt-install(1)
set -ex
test $# -gt 0 && ks_path=$1 || ks_path=${0%/*}/ks.cfg
kscfg=${ks_path##*/}
name=test-guest-from-${kscfg}
connect=${QEMU_CONNECT:-qemu:///system}

virt-install \
--check-cpu --hvm --accelerate --noautoconsole \
--name=${name:?} \
--connect=${connect:?} \
--wait=10 \
--ram=1024 \
--arch=x86_64 \
--vcpus=2 \
--graphics vnc,keymap=us \
--os-type=linux \
--os-variant=rhel7 \
--controller=scsi,model=virtio-scsi \
--location=/var/lib/libvirt/images/rhel-server-7.3-x86_64-dvd.iso \
--initrd-inject=${ks_path} \
--extra-args="ks=file:/${kscfg}" \
--disk pool=default,format=qcow2,cache=none,size=20,bus=scsi \
--network network=default,model=virtio,mac=RANDOM
EOV

echo "[Info] Done"

# vim:sw=4:ts=4:et:
