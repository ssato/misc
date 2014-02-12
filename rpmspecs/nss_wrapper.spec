Name:           nss_wrapper
Version:        1.0.1
Release:        1%{?dist}
Summary:        NSS wrapper library to make an isolated NSS test environment
License:        BSD
URL:            http://cwrap.org/nss_wrapper.html
Source0:        https://ftp.samba.org/pub/cwrap/%{name}-%{version}.tar.gz
BuildRequires:  cmake

%description
Cwrap is a set of tools to create a fully isolated network environment to test
client/server components on a single host. It provides synthetic account
information, hostname resolution and support for privilege separation. The
heart of cwrap consists of three libraries you can preload to any executable.

This package contains nss_wrapper which wraps nss and provides information for
user and group account, allows resolving network names using a custom hosts
file instead of /etc/hosts and DNS, etc.

%package devel
Summary:        Development files of %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Development files for %{name}.

%prep
%setup -q

%build
mkdir build && cd build && %cmake ..
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/pkgconfig
install -d $RPM_BUILD_ROOT%{_libdir}
install -m 644 build/nss_wrapper.pc $RPM_BUILD_ROOT%{_datadir}/pkgconfig
# TODO: Where to install these ?
install -m 644 build/src/libnss_wrapper.so* $RPM_BUILD_ROOT%{_libdir}

# TODO: Implement this.
#%check
#ctest

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README
%{_libdir}/*.so
%{_libdir}/*.so.*

%files devel
%{_datadir}/pkgconfig/%{name}.pc

%changelog
* Wed Feb 12 2014 Satoru SATOH <ssato@redhat.com> - 1.0.1-1
- Initial packaging
