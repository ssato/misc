# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname cbor
%global sumtxt  CBOR loader and dumper for Python
%global desctxt Concise Binary Object Representation (CBOR) is a superset of JSON's schema that's faster and more compact. This package provides python library provides loads()/dumps() like the json standard library.

Name:           python-%{pkgname}
Version:        1.0.0
Release:        2%{?dist}
Summary:        %{sumtxt}
Group:          Development/Libraries
License:        ASL 2.0
URL:            https://bitbucket.org/bodhisnarkva/cbor
Source0:        %{pkgname}-%{version}.tar.gz

%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without python3
%else
%bcond_with python3
%endif

# Available from https://bitbucket.org/bodhisnarkva/cbor/.
Source1:        README.md
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

%description
%{desctxt}

%package     -n python2-%{pkgname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname}
%{desctxt}

%if %{with python3}
%package     -n python3-%{pkgname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname}
%{desctxt}
%endif

%prep
%autosetup -n %{pkgname}-%{version}
cat << EOF > README.md
# From https://github.com/brianolson/cbor_py
Concise Binary Object Representation (CBOR) is a superset of JSON's schema
that's faster and more compact.

* http://tools.ietf.org/html/rfc7049
* http://cbor.io/

This Python implementation provides loads()/dumps() like the json standard
library.
EOF


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
%doc README.md
%{python2_sitearch}/*

%if %{with python3}
%files -n python3-%{pkgname}
%doc README.md
%{python3_sitearch}/*
%endif

%changelog
* Thu Jan 04 2018 Satoru SATOH <ssato@redhat.com> - 1.0.0-2
- Clean up the RPM SPEC

* Fri Feb 24 2017 Satoru SATOH <ssato@redhat.com> - 1.0.0-1
- Initial packaging
