# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname cbor2
%global debug_package %{nil}

%global sumtxt  Pure Python CBOR (de)serializer with extensive tag support
%global desctxt \
Pure python library provides (de)serializer with extensive tag support for\
the Concise Binary Object Representation (CBOR) (RFC 7049) serialization\
format.

Name:           python-%{pkgname}
Version:        4.0.1
Release:        2%{?dist}
Summary:        %{sumtxt}
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/agronholm/cbor2/
Source0:        %{pkgname}-%{version}.tar.gz
Patch0:         cbor2-hardcode-version.patch
BuildArch:      noarch

%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without python3
%else
%bcond_with python3
%endif

%if 0%{?rhel} == 7
BuildRequires:  python-devel
BuildRequires:  python-setuptools
%else
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%endif
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description %{desctxt}

%package     -n python2-%{pkgname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname} %{desctxt}

%if %{with python3}
%package     -n python3-%{pkgname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desctxt}
%endif

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py2_build
%if %{with python3}
%py3_build
%endif

%install
%py2_install
%if %{with python3}
%py3_install
%endif

%files -n python2-%{pkgname}
%doc README.rst
%if 0%{?rhel} == 7
%{python_sitelib}/*
%else
%{python2_sitelib}/*
%endif

%if %{with python3}
%files -n python3-%{pkgname}
%doc README.rst
%{python3_sitelib}/*
%endif

%changelog
* Sun Jan  7 2018 Satoru SATOH <ssato@redhat.com> - 4.0.1-2
- fix: this is noarch package

* Sat Jan  6 2018 Satoru SATOH <ssato@redhat.com> - 4.0.1-1
- Initial packaging
