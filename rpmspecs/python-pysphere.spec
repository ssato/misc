# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname pysphere
%global srcname %{pkgname}
%global sumtxt  Python API for interacting with the vSphere Web Services SDK
%global desc    Python API for interacting with the vSphere Web Services SDK.
%global with_py3k 0

Name:           python-%{pkgname}
Version:        0.1.8
Release:        1%{?dist}
Summary:        %{sumtxt}
Group:          Development/Libraries
License:        BSD
URL:            https://github.com/argos83/%{srcname}
Source0:        %{srcname}-%{version}.zip
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if 0%{?with_py3k}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
%{desc}

%package     -n python2-%{pkgname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{pkgname}
%{desc}

%if 0%{?with_py3k}
%package     -n python3-%{pkgname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{pkgname}
%{desc}
%endif

%prep
%setup -q -n %{srcname}-%{version}

%build
%if 0%{?with_py3k}
%py3_build
%endif
%py2_build

%install
%if 0%{?with_py3k}
%py3_install
%endif
%py2_install

%files -n python2-%{pkgname}
%doc README
%{python2_sitelib}/*

%if 0%{?with_py3k}
%files -n python3-%{pkgname}
%doc README
%{python3_sitelib}/*
%endif

%changelog
* Fri Oct 16 2015 Satoru SATOH <ssato@redhat.com> - 0.1.8-1
- Initial packaging
