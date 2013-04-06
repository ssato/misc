# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define modname errorhandler


Name:           python-%{modname}
Version:        1.1.1
Release:        2%{?dist}
Summary:        A logging framework handler that tracks when messages above a certain level
Group:          Development/Languages
License:        MIT
URL:            http://pypi.python.org/pypi/%{modname}
Source0:        http://pypi.python.org/packages/source/e/%{modname}/%{modname}-%{version}.tar.gz
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

cat << EOF > README.Fedora
quote from the PyPI page:

This is a handler for the python standard logging framework that can be used to
tell whether messages have been logged at or above a certain level.

This can be useful when wanting to ensure that no errors have been logged
before committing data back to a database.

As an example, first, you set up the error handler:

>>> from errorhandler import ErrorHandler
>>> e = ErrorHandler()

Then you can log and check the handler at any point to see if it has been triggered:

>>> e.fired
False
>>> from logging import getLogger
>>> logger = getLogger()
>>> logger.error('an error')
>>> e.fired
True

You can use the fired attribute to only perform actions when no errors have been logged:

>>> if e.fired:
...   print "Not updating files as errors have occurred"
Not updating files as errors have occurred
EOF


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{python_sitelib}/*
%doc README.Fedora


%changelog
* Wed Feb  1 2012 Satoru SATOH <ssato@redhat.com> - 1.1.1-2
- Added README.Fedora (again)
- Embedded source url to make package build easier

* Wed Feb  1 2012 Satoru SATOH <ssato@redhat.com> - 1.1.1-1
- New upstream

* Mon Aug 10 2009 Satoru SATOH <ssato@redhat.com> - 1.0.0-1
- Initial packaging.
