%define srcver 4.03-9411
%define buildarch 64bit

Name:           softether
Version:        4.03_9411
Release:        1%{?dist}
Summary:        An Open-Source Free Cross-platform Multi-protocol VPN Program
License:        GPLv2
URL:            http://www.softether.org
#Source0:        http://jp.softether-download.com/files/softether/v4.03-9411-rtm-2014.01.07-tree/Source%20Code/softether-src-v%{srcver}-rtm.tar.gz
Source0:        softether-src-v%{srcver}-rtm.tar.gz
Patch0:         softether_linux_64_makefile_destdir.patch
BuildRequires:  readline-devel ncurses-devel openssl-devel
Requires:       readline ncurses openssl

%description
SoftEther VPN ("SoftEther" means "Software Ethernet") is one of the world's
most powerful and easy-to-use multi-protocol VPN software. It runs on Windows,
Linux, Mac, FreeBSD and Solaris.

SoftEther VPN is an optimum alternative to OpenVPN and Microsoft's VPN servers.
SoftEther VPN has a clone-function of OpenVPN Server. You can integrate from
OpenVPN to SoftEther VPN smoothly. SoftEther VPN is faster than OpenVPN.
SoftEther VPN also supports Microsoft SSTP VPN for Windows Vista / 7 / 8. No
more need to pay expensive Windows Server license-fee for Remote-Access VPN
function.

%prep
%setup -q -n v%{srcver}
%patch0 -p1 -b.makefile_destdir

%build
cp src/makefiles/linux_%{buildarch}.mak Makefile
make

%install
rm -rf $RPM_BUILD_ROOT
%make_install

%files
%doc AUTHORS.TXT ChangeLog.txt LICENSE.TXT README.TXT THIRD_PARTY.TXT WARNING.TXT
%{_bindir}/vpnbridge
%{_bindir}/vpnclient
%{_bindir}/vpncmd
%{_bindir}/vpnserver
%{_libdir}/softether/vpnbridge/hamcore.se2
%{_libdir}/softether/vpnbridge/vpnbridge
%{_libdir}/softether/vpnclient/hamcore.se2
%{_libdir}/softether/vpnclient/vpnclient
%{_libdir}/softether/vpncmd/hamcore.se2
%{_libdir}/softether/vpncmd/vpncmd
%{_libdir}/softether/vpnserver/hamcore.se2
%{_libdir}/softether/vpnserver/vpnserver

%changelog
* Tue Jan  7 2014 Satoru SATOH <ssato@redhat.com> - 4.03_9411-1
- Initial packaging.
