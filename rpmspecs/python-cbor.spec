# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname cbor
%global desctxt \
Concise Binary Object Representation (CBOR) is a superset of JSON's schema\
that's faster and more compact. This package provides python library provides\
loads()/dumps() like the json standard library.

%bcond_without python2

Name:           python-%{pkgname}
Version:        1.0.0
Release:        4%{?dist}
Summary:        CBOR loader and dumper for Python
Group:          Development/Libraries
License:        ASL 2.0
URL:            https://bitbucket.org/bodhisnarkva/cbor
Source0:        %{pkgname}-%{version}.tar.gz
# Available from https://bitbucket.org/bodhisnarkva/cbor/.
Source1:        README.md
%if %{with python2}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%else
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif
BuildRequires:  gcc

%description    %{desctxt}

%if %{with python2}
%package     -n python2-%{pkgname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname} %{desctxt}
%endif

%package     -n python3-%{pkgname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desctxt}

%prep
%autosetup -n %{pkgname}-%{version}
cp %{SOURCE1} ./

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
%doc README.md
%{python2_sitearch}/*
%endif

%files -n python3-%{pkgname}
%doc README.md
%{python3_sitearch}/*

%changelog
* Fri May  1 2020 Satoru SATOH <satoru.satoh@gmail.com> - 1.0.0-4
- Enable py3 build by default instead of py2
- Fix build time dependencies lacks gcc

* Sat Jan  6 2018 Satoru SATOH <ssato@redhat.com> - 1.0.0-3
- Some more clean ups in the RPM SPEC

* Thu Jan  4 2018 Satoru SATOH <ssato@redhat.com> - 1.0.0-2
- Clean up the RPM SPEC

* Fri Feb 24 2017 Satoru SATOH <ssato@redhat.com> - 1.0.0-1
- Initial packaging
