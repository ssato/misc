%global desc \
This package provides systemd service unit to lanuch iperf on server mode.

Summary: Systemd unit to launch iperf on server mode
Name:    iperf3-server
# https://semver.org
Version: 0.1.0
Release: 1%{?dist}
License: MIT
URL: https://github.com/ssato/misc/rpmspecs
Source0: iperf3-server.service
%{?systemd_requires}
BuildRequires: systemd
BuildArch:     noarch
# https://iperf.fr/iperf-download.php#fedora
# https://iperf.fr/download/fedora/iperf3-3.1.3-1.fc24.x86_64.rpm
Requires:      iperf3
Requires:      systemd

%description  %desc

%prep
%autosetup -T -c %{name}-%{version}
cp %{SOURCE0} ./

%build
cat << EOF > README
%desc
EOF

#cat << EOF > iperf3-server.service
#[Unit]
#Description=Iperf3 running on server mode
#Documentation=man:iperf(3)
#After=network.target
#
#[Service]
#Type=simple
#EnvironmentFile=/etc/sysconfig/iperf3
#ExecStart=/usr/bin/iperf3 --server $IPERF3_OPTIONS
#
## Hardening options:
#PrivateDevices=true
#PrivateTmp=true
#RestrictAddressFamilies=AF_INET AF_INET6
## .. note:: These are not available in RHEL =< 8.
##MemoryDenyWriteExecute=yes
##PrivateMounts=true
##RestrictRealtime=yes
##RestrictSUIDSGID=yes
##ProtectControlGroups=true
#EOF

cat << EOF > iperf3
# .. seealso:: iperf3(1)
IPERF3_OPTIONS="-V"
EOF

%install
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}/etc/sysconfig

install -m 644 iperf3-server.service %{buildroot}%{_unitdir}
install -m 644 iperf3 %{buildroot}/etc/sysconfig

%check
:

%post
%systemd_post iperf3-server.service

%preun
%systemd_preun iperf3-server.service

%postun
%systemd_postun_with_restart iperf3-server.service

%files
%doc README
%config /etc/sysconfig/iperf3
%{_unitdir}/iperf3-server.service

%changelog
* Mon Jan 13 2020 Satoru SATOH <ssato@redhat.com> - 0.1.0-1
- Initial build.
