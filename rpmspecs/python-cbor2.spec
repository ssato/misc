# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname cbor2

%global desctxt \
Pure python library provides (de)serializer with extensive tag support for\
the Concise Binary Object Representation (CBOR) (RFC 7049) serialization\
format.

%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-%{pkgname}
Version:        4.1.0
Release:        1%{?dist}
Summary:        Pure Python CBOR (de)serializer with extensive tag support
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/agronholm/cbor2
Source0:        %{pkgname}-%{version}.tar.gz
Patch0:         cbor2-hardcode-version.patch
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description %{desctxt}

%package     -n python2-%{pkgname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname} %{desctxt}

%if %{with python3}
%package     -n python3-%{pkgname}
Summary:        %{summary}
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
* Tue Jul  3 2018 Satoru SATOH <ssato@redhat.com> - 4.1.0-1
- fix: clean up the RPM SPEC like python-anyconfig does

* Sun Jan  7 2018 Satoru SATOH <ssato@redhat.com> - 4.0.1-2
- fix: this is noarch package

* Sat Jan  6 2018 Satoru SATOH <ssato@redhat.com> - 4.0.1-1
- Initial packaging
