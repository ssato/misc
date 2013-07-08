# How to build this:
#
# 0. git clone https://github.com/caleb-/evilvte.git evilvte.git  [in this dir]
# 1. tar --xz -cvf evilvte.git.tar.xz
# 2. builsrpm evilvte.spec [in this dir]
# 3. mock evilvte-x.y.z-a.b.c.src.rpm
#

# TODO:
# It's still failed to build in RHEL 6.4 env with this error:
#  ... undefined reference to `gdk_window_get_display'.

%define gitrev 9abeb9ad38

Name:           evilvte
Version:        0.5.2pre1.%{gitrev}
Release:        1%{?dist}
Summary:        VTE based highly customizable and lightweight terminal emulator
License:        GPLv2
URL:            http://www.calno.com/evilvte/
Source0:        %{name}.git.tar.xz
Patch0:         evilvte-custom.patch
%if 0%{?rhel}
BuildRequires:  gtk2-devel
BuildRequires:  glib2-devel
BuildRequires:  vte-devel
Requires:       gtk2, glib2, vte
%else
BuildRequires:  gtk3-devel
BuildRequires:  vte3-devel
Requires:       gtk3, vte3
%endif


%description
Evilvte is a VTE based, highly customizable and very lightweight terminal
emulator.

Features: tabs, tabbar autohide, right click to switch encoding, supports
almost all VTE features and build-time configuration.


%prep
%setup -q -n %{name}.git
%patch0 -p1 -b .custom


%build
%if 0%{?rhel}
./configure --prefix=/usr --with-gtk=2.0
%else
./configure --prefix=/usr --with-gtk=3.0
%endif
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
