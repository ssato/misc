# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname check-manifest
%global srcname check-manifest
%global desctxt \
A tool to check the completeness of MANIFEST.in for Python packages.

Name:           python-%{pkgname}
Version:        0.39
Release:        1%{?dist}
Summary:        Tool checking MANIFEST.in for python packages
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/mgedmin/check-manifest
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
%{python2_sitelib}/*
%{_bindir}/*
%endif

%files -n python3-%{pkgname}
%doc README.rst
%{python3_sitelib}/*
%{_bindir}/*

%changelog
* Tue Jul 16 2019 Satoru SATOH <ssato@redhat.com> - 0.39-1
- Initial packaging
