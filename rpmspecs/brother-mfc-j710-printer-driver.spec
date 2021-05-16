%global  pmodel mfcj710d
%global  src %{pmodel}cupswrapper-src
%global  sver 3.0.0-1

Name:           brother-mfc-j710d-printer-driver
Summary:        Drivers for Brother MFC J710D inkjet printer
Version:        3.0.0.1
Release:        1%{?dist}
License:        GPLv2+
URL:            https://support.brother.co.jp/j/b/downloadhowto.aspx
Source0:        https://download.brother.com/welcome/dlf100808/%{src}-%{sver}.tar.gz
Patch0:         %{src}-makefile.patch
BuildRequires:  gcc
BuildRequires:  gzip
BuildRequires:  make

Requires:       cups-filesystem

%description
This package contains drivers for Brother J710D Inkjet printer.

%prep
%autosetup -n %{src}-%{sver} -p1

%build
export CFLAGS="${RPM_OPT_FLAGS}"
export CXXFLAGS="${RPM_OPT_FLAGS}"
make %{?_smp_mflags} -C brcupsconfig/

%install
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_datadir}/cups/model/Brother/

for x in brcupsconfig/brcupsconfpt1 cupswrapper/cupswrapper%{pmodel}
do
  install -m 755 $x %{buildroot}%{_sbindir}/
done

for ppd in ppd/*.ppd
do
  install -m 644 $ppd %{buildroot}%{_datadir}/cups/model/Brother/
  gzip -v9 %{buildroot}%{_datadir}/cups/model/Brother/*.ppd
done

%files
%{_sbindir}/*
%{_datadir}/cups/model/Brother/*.ppd.gz

%changelog
* Sun May 16 2021 Satoru SATOH <satoru.satoh@gmail.com> - 3.0.0.1-1
- First release.
