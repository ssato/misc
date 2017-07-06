#! /bin/bash
#
# Make a RPM to provide access to yum repos of RPMs in ISO image.
#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
# Requirements: isoinfo (genisoimage), rpmbuild (rpm-build)
#
set -e

USAGE="Usage: $0 [Options ...] RPMS_ISO_IMAGE_PATH"

iso_install_dir=/srv/iso-images/
iso_mntdir=/srv/iso-mnt/
mnt_options=ro,loop

show_help () {
    cat << EOH
$USAGE
Options:
    -n NAME             Specify Yum Repo name (id)
    -w WORKDIR          Specify working dir to save results
    -d ISO_INSTALL_DIR  Dir to install given iso image [${iso_install_dir:?}]
    -m ISO_MNTDIR       Dir to mount given iso image [${iso_mntdir:?}]
    -o MNT_OPTIONS      Mount options [${mnt_options}]

    -h                  Show this help text
EOH
}

gen_rpm_spec () {
    local iso_install_path=$1
    local iso_mntdir=$2
    local name=$3
    local workdir=$4
    local mnt_options=${5:-ro,loop}

    local iso_basename=${iso_install_path##*/}

cat << EOS > ${workdir:?}/package.spec
%global desc Yum repo data and configuration for ${iso_basename:?}
%global httpd_confdir %{_sysconfdir}/httpd/conf.d
%global repofile %{_sysconfdir}/yum.repos.d/iso-images-${name}.repo

Name:           ${name:?}
Summary:        %{desc}
Version:        1.0
Release:        1%{?dist}
License:        Commercial
URL:            https://github.com/ssato/misc/
Group:          System Environment/Base
Source0:        ${iso_basename}
Requires:       systemd-units
BuildRequires:  systemd
BuildRequires:  genisoimage
BuildArch:      noarch

%description
%{desc}

%prep
%setup -T -c %{name}-%{version}

%build
cat << EOD > README
%{desc} built at $(date --rfc-2822)
EOD

%package        -n httpd-data
Summary:        %{desc} - httpd data files
Requires:       %{name}
Requires:       httpd

%description    -n httpd-data
%{desc}

This package contains data for apache httpd.

%install
mkdir -p %{buildroot}/${iso_install_path}
mkdir -p %{buildroot}/${iso_mntdir}
mkdir -p %{buildroot}/%{_unitdir}
mkdir -p %{buildroot}/\$(dirname %{repofile})
mkdir -p %{buildroot}/%{httpd_confdir}

install -m 644 %{SOURCE0} %{buildroot}/${iso_install_path}

cat << EOU > %{buildroot}/%{_unitdir}/iso-images-${name}.mount
[Unit]
Description=Mount ISO image ${iso_basename}
After=local-fs.target
ConditionPathExists=${iso_install_path:?}

[Mount]
What=${iso_install_path}
Where=${iso_mntdir:?}
Options=${mnt_options:?}
EOU

cat << EOU > %{buildroot}/%{_unitdir}/iso-images-${name}.automount
[Unit]
Description=Mount ISO image ${iso_basename} automatically

[AutoMount]
Where=${iso_mntdir:?}
EOU

cat << EOC > %{buildroot}/%{repofile}
[${name}]
name=${name} (${iso_basename})
baseurl=file://${iso_mntdir}
enabled=1
# FIXME:
gpgcheck=0

EOC
for subdir in \$(isoinfo -f -i %{SOURCE0} | sed -n '/repodata$/s/\/repodata//p'); do
    rid=${name}\${subdir//\//-}
    cat << EOC >> %{buildroot}/%{repofile}
[\${rid}-iso]
name=${name} - \${subdir}
baseurl=file://${iso_mntdir}/\${subdir}
enabled=1
# FIXME:
gpgcheck=0

EOC
done

cat << EOC > %{buildroot}/%{httpd_confdir}/iso-images-${name}.conf
Alias /${name} ${iso_mntdir}
<Location "/${name}">
    #Options All
    #AllowOverride All
    Require ip ::1
    Require ip 127.0.0.1
    Options Indexes FollowSymLinks
</Location>
EOC

%files
%dir ${iso_mntdir}
${iso_install_path}
%{_unitdir}/*.*
%config %{repofile}
%doc README

%files          -n httpd-data
%{httpd_confdir}/iso-images-${name}.conf

%changelog
* $(LANG=en_US.UTF-8 date "+%a %b %_d %Y") $0 <$(id -nu)@localhost.localdomain> - 1.0-1
- Initial packaging
EOS
}

build_srpm () {
    local workdir=$1

    rpmbuild -bs \
        --define "_topdir ${workdir:?}" \
        --define "_srcrpmdir ${workdir}" \
        --define "_sourcedir ${workdir}" \
        --define "_buildroot ${workdir}/build" \
    ${workdir}/package.spec

    echo "[Info] Build srpm in ${workdir}"
}


# main:
while getopts "n:w:d:m:n:o:h" opt
do
  case $opt in
    n) name=$OPTARG ;;
    w) workdir=$OPTARG ;;
    d) iso_install_dir=$OPTARG ;;
    m) iso_mntdir=$OPTARG ;;
    o) mnt_options=$OPTARG ;;
    h) show_help; exit 0 ;;
    \?) show_help; exit 1 ;;
  esac
done
shift $(($OPTIND - 1))

test $# -ge 1 || { echo "$USAGE"; exit 1; }

ISO_PATH=$1
ISO_BASENAME=${ISO_PATH##*/}

test -f ${ISO_PATH} || { echo "[Error] ${ISO_PATH} does not exist"; exit 1; }


NAME=${name:-${ISO_BASENAME/.iso/}}
ISO_INSTALL_PATH=${iso_install_dir:?}/${ISO_BASENAME}
ISO_MNTDIR=${iso_mntdir:?}/${NAME}
WORKDIR=${workdir:-$(mktemp -d ${NAME}-workdir)}

echo "[Info] Generate RPM SPEC in ${WORKDIR}"
gen_rpm_spec ${ISO_INSTALL_PATH:?} ${ISO_MNTDIR:?} ${NAME:?} ${WORKDIR:?} ${mnt_options:?}

echo "[Info] Arrange ${ISO_BASENAME} in ${WORKDIR}"
test -f ${WORKDIR}/${ISO_BASENAME} || (cd ${WORKDIR} && ln -s ${ISO_PATH} ./)

echo "[Info] Build Source RPM in ${WORKDIR}"
build_srpm ${WORKDIR}

# vim:sw=4:ts=4:et:
