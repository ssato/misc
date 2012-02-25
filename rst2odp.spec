# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}


Name:           rst2odp
Version:        0.2.3
Release:        1%{?dist}
Summary:        Convert reStructuredText files to Openoffice Impress (odp) files
Group:          Applications/Text
License:        ASL 2.0
URL:            http://pypi.python.org/pypi/rst2odp
Source0:        http://pypi.python.org/packages/source/r/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools


%description
Converter for rst to OpenOffice Impress

Packaging of rst2odp and opdlib from docutils sandbox. odplib is a standalone
library for creating odp output from python. rst2odp wraps it for rst users.


%prep
%setup -q


%build
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{python_sitelib}/*
%{_bindir}/*


%changelog
* Sun Feb 26 2012 Satoru SATOH <ssato@redhat.com> - 0.2.3-1
- Initial packaging.
