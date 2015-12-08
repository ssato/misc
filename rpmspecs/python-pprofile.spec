%global srcname pprofile
%global sumtxt  Line-granularity, thread-aware deterministic and statistic pure-python profiler
%global desctxt Line-granularity, thread-aware deterministic and statistic pure-python profiler, inspired from Robert Kern's line_profiler.

Name:           python-%{srcname}
Version:        1.7.3
Release:        1%{?dist}
Summary:        %{sumtxt}
License:        GPLv2+
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
%doc README.rst demo/
%{_bindir}/*
%{python2_sitelib}/*

%changelog
* Mon Dec  7 2015 Satoru SATOH <ssato@redhat.com> - 1.7.3-1
- Initial packaging
