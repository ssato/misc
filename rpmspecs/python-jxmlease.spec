# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname jxmlease
%global srcname jxmlease
%global desctxt \
A Python module for converting XML to intelligent Python data structures, \
and converting Python data structures to XML

Name:           python-%{pkgname}
Version:        1.0.1
Release:        2%{?dist}
Summary:        Python library converting XML from/to python objects
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/Juniper/jxmlease
Source0:        %{srcname}-%{version}.tar.gz
BuildArch:      noarch

%if 0%{?rhel} == 7 || 0%{?epel} == 7
%bcond_without python2
%else
%bcond_with python2
%endif

%if %{with python2}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%endif
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description    %{desctxt}

%if %{with python2}
%package     -n python2-%{pkgname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname} %{desctxt}
%endif

%package     -n python3-%{pkgname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desctxt}

%prep
%autosetup -n %{srcname}-%{version}

%build
%if %{with python2}
%py2_build
%endif
%py3_build

%install
%if %{with python2}
%py2_install
%endif
%py3_install

%if %{with python2}
%files -n python2-%{pkgname}
%doc README.rst
%doc docs
%{python2_sitelib}/*
%endif

%files -n python3-%{pkgname}
%doc README.rst
%doc docs
%{python3_sitelib}/*

%changelog
* Tue Jul 16 2019 Satoru SATOH <ssato@redhat.com> - 1.0.1-2
- fix: s/sumtxt/summary/g
- disable python2 and enable python3 builds by default

* Mon Jul 15 2019 Satoru SATOH <ssato@redhat.com> - 1.0.1-1
- Initial packaging
