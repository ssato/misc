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
