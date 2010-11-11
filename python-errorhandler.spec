# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}


Name:           python-errorhandler
Version:        1.0.0
Release:        1%{?dist}
Summary:        A logging framework handler that tracks when messages above a certain level
Group:          Development/Languages
License:        MIT
URL:            http://pypi.python.org/pypi/errorhandler
Source0:        errorhandler-%{version}.tar.gz
Source1:        README.Fedora.rst
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools


%description
A logging framework handler that tracks when messages above a certain level
have been logged.

This is a handler for the python standard logging framework that can be used to
tell whether messages have been logged at or above a certain level.

This can be useful when wanting to ensure that no errors have been logged
before committing data back to a database.


%prep
%setup -q -n errorhandler-%{version}


%build
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
cp %SOURCE1 ./


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.Fedora.rst
%{python_sitelib}/*


%changelog
* Mon Aug 10 2009 Satoru SATOH <ssato@redhat.com> - 1.0.0-1
- Initial packaging.
