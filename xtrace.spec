Name:           xtrace
Version:        1.0.1
Release:        1%{?dist}
Summary:        trace communication between X client and server
Group:          Development/Debuggers
License:        GPLv2
URL:            http://xtrace.alioth.debian.org
Source0:        https://alioth.debian.org/frs/download.php/3149/xtrace_1.0.1.orig.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#BuildRequires:  xorg-x11-proto-devel
Requires:       xorg-x11-xauth


%description
What strace is for system calls, xtrace is for X11 connections: you hook it
between one or more X11 clients and an X server and it prints the requests
going from client to server and the replies, events and errors going the other
way. 


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/xtrace/*


%changelog
* Tue Sep 17 2009 Satoru SATOH <ssato@redhat.com> - 1.0.1-1
- Initial package.
