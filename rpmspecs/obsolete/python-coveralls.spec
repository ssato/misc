# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-coveralls
Version:        2.5.0
Release:        1%{?dist}
Summary:        A python module to interface with the coveralls.io API
Group:          Development/Languages
License:        ASL 2.0
URL:            http://pypi.python.org/pypi/python-coveralls
Source0:        http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       PyYAML
Requires:       python-requests
Requires:       python-coverage
Requires:       python-six
Requires:       python-sh
# for testing:
#Requires:       python-pytest
#Requires:       python-pytest-pep8
#Requires:       python-pytest-cov
#Requires:       python-httpretty

%description
This package provides a module to interface with the https://coveralls.io API.

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%if 0%{?rhel} && 0%{?rhel} <= 5
%clean
rm -rf $RPM_BUILD_ROOT
%endif

%files
%defattr(-,root,root,-)
%doc README.rst
%{python_sitelib}/*
%{_bindir}/*

%changelog
* Sun May 31 2015 Satoru SATOH <ssato@redhat.com> - 2.5.0-1
- New upstream

* Fri Oct  3 2014 Satoru SATOH <ssato@redhat.com> - 2.4.2-1
- Initial packaging.
