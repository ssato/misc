# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname rtyaml
%global sumtxt Enhanced version of YAML parser and emitter for Python
%global desctxt This module provides wrappers around pyyaml to set sane defaults: \
- round-tripping YAML files is possible by preserving field order \
- saner output defaults are set for strings \
- a comment block found at the very beginning of a stream when loading YAML is preserved when writing it back out

Name:           python-%{pkgname}
Version:        0.0.3
Release:        1%{?dist}
Summary:        %{sumtxt}
Group:          Development/Libraries
License:        Public Domain
URL:            https://pypi.python.org/pypi/rtyaml
Source0:        %{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel python3-devel
BuildRequires:  python-setuptools python3-setuptools

%description
%{desctxt}

%package     -n python2-%{pkgname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname}
%{desctxt}

%package     -n python3-%{pkgname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname}
%{desctxt}

%prep
%setup -q -n %{pkgname}-%{version}

%build
%py3_build
%py2_build

%install
%py3_install
%py2_install

%files -n python2-%{pkgname}
%doc README.rst
%{python2_sitelib}/*

%files -n python3-%{pkgname}
%doc README.rst
%{python3_sitelib}/*

%changelog
* Sat Feb 25 2017 Satoru SATOH <ssato@redhat.com> - 0.0.3-1
- Initial packaging
