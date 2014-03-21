Name:           terminology
Version:        0.5.0
Release:        1%{?dist}
License:        BSD
Summary:        EFL based terminal emulator
Url:            http://www.enlightenment.org
Group:          User Interface/Desktops
Source:         http://download.enlightenment.org/rel/apps/%{name}/%{name}-%{version}.tar.gz
BuildRequires:  desktop-file-utils
#BuildRequires:  ecore-devel
#BuildRequires:  edje-devel
#BuildRequires:  efreet-devel
#BuildRequires:  ethumb-devel
#BuildRequires:  evas-devel
#BuildRequires:  libeina-devel
BuildRequires:  efl-devel
BuildRequires:  elementary-devel
Requires:       terminus-fonts 
Requires:       xorg-x11-fonts-misc

%description
Fast and lightweight terminal emulator using EFL libraries.

%prep
%setup -q

%build
%configure --disable-silent-rules
make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot} INSTALL="/usr/bin/install -p"

#Remove fonts that already exist in Fedora
rm -rf %{buildroot}%{_datadir}/terminology/fonts/10x20.pcf
rm -rf %{buildroot}%{_datadir}/terminology/fonts/4x6.pcf
rm -rf %{buildroot}%{_datadir}/terminology/fonts/5x7.pcf
rm -rf %{buildroot}%{_datadir}/terminology/fonts/5x8.pcf
rm -rf %{buildroot}%{_datadir}/terminology/fonts/6x10.pcf
rm -rf %{buildroot}%{_datadir}/terminology/fonts/6x12.pcf
rm -rf %{buildroot}%{_datadir}/terminology/fonts/6x13.pcf
rm -rf %{buildroot}%{_datadir}/terminology/fonts/6x9.pcf
rm -rf %{buildroot}%{_datadir}/terminology/fonts/7x13.pcf
rm -rf %{buildroot}%{_datadir}/terminology/fonts/7x14.pcf
rm -rf %{buildroot}%{_datadir}/terminology/fonts/8x13.pcf
rm -rf %{buildroot}%{_datadir}/terminology/fonts/9x15.pcf
rm -rf %{buildroot}%{_datadir}/terminology/fonts/9x18.pcf
rm -rf %{buildroot}%{_datadir}/terminology/fonts/terminus-*

desktop-file-validate %{buildroot}/%{_datadir}/applications/terminology.desktop

%files
%doc README COPYING
%{_mandir}/man1/*
%{_bindir}/tyalpha
%{_bindir}/tybg
%{_bindir}/tycat
%{_bindir}/tyls
%{_bindir}/typop
%{_bindir}/tyq
%{_bindir}/terminology
%{_datadir}/applications/terminology.desktop
%{_datadir}/icons/terminology.png
%{_datadir}/terminology

%changelog
* Fri Mar 21 2014 Satoru SATOH <satoru.satoh@gmail.com> - 0.5.0-1
- Update to 0.5.0 (thanks Conrad Meyer)

* Tue Dec 10 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 0.4.0-1
- Update to 0.4.0 (thanks Conrad Meyer)

* Sun Oct 13 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 0.3.0-3
- Remove post scriptlets as per review.

* Wed Oct 09 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 0.3.0-2
- Remove bundled fonts that already exist in Fedora.
- Add icon and desktop scriptlets

* Tue Oct 08 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 0.3.0-1
- Update to 0.3.0
- Fix license
- Update BRs

* Wed Jan 02 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 0.2.0-1
- initial spec
