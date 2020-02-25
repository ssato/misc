%global pkgname memory_profiler

Name:           python3-%{pkgname}
Version:        0.57.0
Release:        1%{?dist}
Summary:        A module for monitoring memory usage of a python program
License:        BSD
Group:          Development/Languages
URL:            https://github.com/pythonprofilers/memory_profiler
Source0:        https://pypi.python.org/packages/source/m/%{pkgname}/%{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3-psutil

%description
This is a python module for monitoring memory consumption of a process as well
as line-by-line analysis of memory consumption for python programs.

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py3_build

%install
%py3_install

%files
%doc README.rst
%{python3_sitelib}/*
%{_bindir}/*

%changelog
* Wed Feb 26 2020 Satoru SATOH <satoru.satoh@gmail.com> - 0.57.0-1
- new upstream release
- cleanup the RPM SPEC and only support python3

* Sun Dec 13 2015 Satoru SATOH <ssato@redhat.com> - 0.39-1
- Latest upstream release

* Wed Jan 28 2015 Satoru SATOH <ssato@redhat.com> - 0.32-1
- Initial packaging
