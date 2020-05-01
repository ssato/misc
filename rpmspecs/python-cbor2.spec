# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname cbor2
%global desctxt \
Pure python library provides (de)serializer with extensive tag support for\
the Concise Binary Object Representation (CBOR) (RFC 7049) serialization\
format.

%bcond_with python2

Name:           python-%{pkgname}
Version:        5.1.0
Release:        1%{?dist}
Summary:        Python library to encode and decode the CBOR data
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/agronholm/cbor2
Source0:        %{pkgname}-%{version}.tar.gz
Patch0:         cbor2-detect-libc-ver-hack.patch
#BuildArch:      noarch
BuildRequires:  gcc
%if %{with python2}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-setuptools_scm
%endif
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm

%description %{desctxt}

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
%autosetup -n %{pkgname}-%{version}

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
# No ext modules for py2.
%{python2_sitelib}/*
%endif

%files -n python3-%{pkgname}
%doc README.rst
%{python3_sitearch}/*

%changelog
* Fri May  1 2020 Satoru SATOH <satoru.satoh@rgmail.com> - 5.1.0-1
- new upstream
- fix: enable py3 by default instead of py2
- fix: remove macro hack for RHEL 7; drop its support
- fix: upstream now has ext_module so that this is not noarch any more
- fix: add build time dependency to gcc

* Tue Jul  3 2018 Satoru SATOH <ssato@redhat.com> - 4.1.0-1
- fix: clean up the RPM SPEC like python-anyconfig does

* Sun Jan  7 2018 Satoru SATOH <ssato@redhat.com> - 4.0.1-2
- fix: this is noarch package

* Sat Jan  6 2018 Satoru SATOH <ssato@redhat.com> - 4.0.1-1
- Initial packaging
