%define gitrev 9abeb9ad38

Name:           evilvte
Version:        0.5.2pre1.%{gitrev}
Release:        1%{?dist}
Summary:        VTE based highly customizable and lightweight terminal emulator
License:        GPLv2
URL:            http://www.calno.com/evilvte/
Source0:        %{name}.git.tar.xz
Patch0:         evilvte-custom.patch
BuildRequires:  gtk3-devel
BuildRequires:  vte3-devel
Requires:       gtk3, vte3


%description
Evilvte is a VTE based, highly customizable and very lightweight terminal
emulator.

Features: tabs, tabbar autohide, right click to switch encoding, supports
almost all VTE features and build-time configuration.


%prep
%setup -q -n %{name}.git
%patch0 -p1 -b .custom


%build
./configure --prefix=/usr --with-gtk=3.0
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
gzip -v9 $RPM_BUILD_ROOT%{_datadir}/man/man1/*.1


%files
%doc ChangeLog
%{_bindir}/*
%{_datadir}/applications/evilvte.desktop
%{_datadir}/gnome-control-center/default-apps/evilvte.xml
%{_datadir}/icons/hicolor/*/apps/evilvte.*
%{_datadir}/pixmaps/evilvte.png
%{_datadir}/man/man1/*


%changelog
* Mon Jul  8 2013 Satoru SATOH <ssato@redhat.com> - 0.5.2pre1.9abeb9ad38-1
- Initial packaging
