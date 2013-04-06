Name:           trayer
Version:        1.1.4
Release:        1%{?dist}
Summary:        Lightweight GTK2-based systray for UNIX desktop
License:        GPLv2
#URL:            http://code.google.com/p/trayer/
URL:            https://github.com/sargon/trayer-srg
#Source0:        %{name}-%{version}.tgz
Source0:        sargon-trayer-srg-trayer-1.1.4-3-gb04805f.tar.gz
BuildRequires:  libXmu-devel, gtk2-devel
#Requires:       


%description
trayer is a small program designed to provide systray functionality present in
GNOME/KDE desktop environments for window managers which do not support that
function. System tray is a place, where various applications put their icons,
so they are always visible presenting status of applications and allowing user
to control programs. 


%prep
%setup -q -n sargon-trayer-srg-b04805f


%build
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
#make install DESTDIR=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -m 755 trayer $RPM_BUILD_ROOT%{_bindir}


%files
%doc README CHANGELOG CREDITS 
%{_bindir}/trayer


%changelog
* Sat Jan 14 2012 Satoru SATOH <ssato@redhat.com> - 1.1.4-1
- Initial packaging.
