%global srcname pyprof2calltree
%global sumtxt  Help visualize profiling data from cProfile with kcachegrind
%global desctxt Help visualize profiling data from cProfile with kcachegrind and qcachegrind.

Name:           python-%{srcname}
Version:        1.3.2
Release:        1%{?dist}
Summary:        %{sumtxt}
License:        BSD
Group:          Development/Languages
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        https://pypi.python.org/packages/source/p/%{srcname}/%{srcname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-tools

%description
%{desctxt}

%prep
%autosetup -n %{srcname}-%{version}

%build
%py2_build

%install
%py2_install

%files
%doc README.txt
%{_bindir}/*
%{python2_sitelib}/*

%changelog
* Thu Dec  3 2015 Satoru SATOH <ssato@redhat.com> - 1.3.2-1
- Initial packaging
