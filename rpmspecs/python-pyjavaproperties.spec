%global debug_package %{nil}
%global pkgname pyjavaproperties
%global sumtxt Python library to parse and manipulate Java properties files

Name:           python-%{pkgname}
Version:        0.6
Release:        1%{?dist}
Summary:        %{sumtxt}
Group:          Development/Languages
License:        Python
URL:            http://pypi.python.org/pypi/%{pkgname}
Source0:        http://pypi.python.org/packages/source/p/%{pkgname}/%{pkgname}-%{version}.tar.gz
BuildArch:      noarch

%global desctxt \
This module is designed to be a python equivalent to the java.util.Properties\
class. Currently, the basic input/output methods are supported, and there are\
plans to add the XML input/output methods found in J2SE 5.0.\
\
Fundamentally, this module is designed so that users can easily parse and\
manipulate Java Properties files - that's it. There's a fair number of us\
pythonistas who work in multi-language shops, and constantly writing your own\
parsing mechanism is just painful. Not to mention Java guys are notoriously\
unwilling to use anything which is cross-language for configuration, unless\
it's XML, which is a form of self-punishment. :)

%description %{desctxt}

%package     -n python2-%{pkgname}
Summary:        %{sumtxt}
%if 0%{?rhel} == 7
BuildRequires:  python-devel
BuildRequires:  python-setuptools
%else
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%endif

%description -n python2-%{pkgname} %{desctxt}

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py2_build

%install
%py2_install

%clean
rm -rf $RPM_BUILD_ROOT


%files -n python2-%{pkgname}
%defattr(-,root,root,-)
%doc README TODO testdata
%{python_sitelib}/*


%changelog
* Sun Jul 22 2012 Satoru SATOH <ssato@redhat.com> - 0.6-1
- Initial packaging.
