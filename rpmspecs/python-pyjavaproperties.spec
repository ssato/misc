%global debug_package %{nil}
%global pkgname pyjavaproperties

Name:           python-%{pkgname}
Version:        0.6
Release:        1%{?dist}
Summary:        Python replacement for java.util.Properties
Group:          Development/Languages
License:        Python
URL:            http://pypi.python.org/pypi/%{pkgname}
Source0:        http://pypi.python.org/packages/source/p/%{pkgname}/%{pkgname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools


%description
This module is designed to be a python equivalent to the java.util.Properties
class. Currently, the basic input/output methods are supported, and there are
plans to add the XML input/output methods found in J2SE 5.0.

Fundamentally, this module is designed so that users can easily parse and
manipulate Java Properties files - that's it. There's a fair number of us
pythonistas who work in multi-language shops, and constantly writing your own
parsing mechanism is just painful. Not to mention Java guys are notoriously
unwilling to use anything which is cross-language for configuration, unless
it's XML, which is a form of self-punishment. :)


%prep
%setup -q -n %{pkgname}-%{version}


%build
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT/pyjavaproperties.egg-info/
 

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README TODO testdata
%{python_sitelib}/*


%changelog
* Sun Jul 22 2012 Satoru SATOH <ssato@redhat.com> - 0.6-1
- Initial packaging.
