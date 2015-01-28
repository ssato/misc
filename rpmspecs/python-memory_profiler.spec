# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%define debug_package %{nil}

%if 0%{?fedora}
%global with_python3 1
%endif

%global pkgname memory_profiler

Name:           python-%{pkgname}
Version:        0.32
Release:        1%{?dist}
Summary:        A module for monitoring memory usage of a python program
License:        BSD
Group:          Development/Languages
URL:            http://pypi.python.org/pypi/%{pkgname}
Source0:        https://pypi.python.org/packages/source/m/%{pkgname}/%{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-psutil
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3-psutil
%endif

%description
This is a python module for monitoring memory consumption of a process as well
as line-by-line analysis of memory consumption for python programs.

%if 0%{?with_python3}
%package -n     python3-%{pkgname}
Summary:        A module for monitoring memory usage of a python program

%description -n python3-%{pkgname}
This is a python module for monitoring memory consumption of a process as well
as line-by-line analysis of memory consumption for python programs.

This is a package for python-3.
%endif

%prep
%setup -q -n %{pkgname}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
sed -e '1s,/usr/bin/env python,/usr/bin/python3,g' $RPM_BUILD_ROOT/%{_bindir}/mprof > $RPM_BUILD_ROOT/%{_bindir}/py3mprof
popd
%endif
 
%files
%doc README.rst
%{python_sitelib}/*
%{_bindir}/mprof

%if 0%{?with_python3}
%files -n       python3-%{pkgname}
%defattr(644,root,root,755)
%doc README.rst
%{python3_sitelib}/*
%{_bindir}/py3mprof
%endif

%changelog
* Wed Jan 28 2015 Satoru SATOH <ssato@redhat.com> - 0.32-1
- Initial packaging
