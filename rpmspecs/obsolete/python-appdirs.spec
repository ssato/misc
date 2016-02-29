# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define  pkg  appdirs

Name:           python-%{pkg}
Version:        1.4.0
Release:        1%{?dist}
Summary:        A small Python module for determining appropriate configuration dirs
Group:          Applications/System
License:        MIT
URL:            http://pypi.python.org/pypi/appdirs
Source0:        http://pypi.python.org/packages/source/a/appdirs/appdirs-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools

%description
A small Python module for determining appropriate " + "platform-specific dirs,
e.g. a "user data dir".

%prep
%setup -q -n appdirs-%{version}

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README.rst
%{python_sitelib}/*

%changelog
* Tue Nov 11 2014 Satoru SATOH <ssato@redhat.com> - 1.4.0-1
- Initial packaging.
