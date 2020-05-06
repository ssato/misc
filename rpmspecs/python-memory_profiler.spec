%global pkgname memory_profiler
%global desctxt \
This is a python module for monitoring memory consumption of a process as well \
as line-by-line analysis of memory consumption for python programs.

Name:           python-%{pkgname}
Version:        0.57.0
Release:        3%{?dist}
Summary:        A module for monitoring memory usage of a python program
License:        BSD
Group:          Development/Languages
URL:            https://github.com/pythonprofilers/memory_profiler
Source0:        https://pypi.python.org/packages/source/m/%{pkgname}/%{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description %{desctxt}

%package     -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-psutil
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desctxt}

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{pkgname}
%doc README.rst
%{python3_sitelib}/*
%{_bindir}/*

%changelog
* Thu May  7 2020 Satoru SATOH <satoru.satoh@gmail.com> - 0.57.0-3
- Build python3-... package

* Wed May  6 2020 Satoru SATOH <satoru.satoh@gmail.com> - 0.57.0-3
- cleanup this RPM SPEC more

* Wed Feb 26 2020 Satoru SATOH <satoru.satoh@gmail.com> - 0.57.0-1
- new upstream release
- cleanup the RPM SPEC and only support python3

* Sun Dec 13 2015 Satoru SATOH <ssato@redhat.com> - 0.39-1
- Latest upstream release

* Wed Jan 28 2015 Satoru SATOH <ssato@redhat.com> - 0.32-1
- Initial packaging
