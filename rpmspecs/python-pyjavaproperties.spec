%global debug_package %{nil}
%global pkgname pyjavaproperties
%global sumtxt Python library to parse and manipulate Java properties files

Name:           python-%{pkgname}
Version:        0.6
Release:        2%{?dist}
Summary:        %{sumtxt}
Group:          Development/Languages
License:        Python
URL:            http://pypi.python.org/pypi/%{pkgname}
Source0:        http://pypi.python.org/packages/source/p/%{pkgname}/%{pkgname}-%{version}.tar.gz
BuildArch:      noarch

%global desctxt \
This is a python library to parse and manipulate Java properties files like\
java.util.Properties does.

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
rm -f pyjavaproperties_test.py  # Remove to avoid it'll be installed.
sed -i '1d' pyjavaproperties.py  # It's not executable.

%build
%py2_build

%install
%py2_install

%files -n python2-%{pkgname}
%defattr(-,root,root,-)
%doc README TODO testdata
%{python_sitelib}/*

%changelog
* Sat Jan  6 2018 Satoru SATOH <ssato@redhat.com> - 0.6-2
- Cleanup and simplify this RPM SPEC to comply w/ the current Fedora guidelines

* Sun Jul 22 2012 Satoru SATOH <ssato@redhat.com> - 0.6-1
- Initial packaging.
