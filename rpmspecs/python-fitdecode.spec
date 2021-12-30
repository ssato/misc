# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname fitdecode
%global desctxt \
A FIT file parsing and decoding library.

Name:           python-%{pkgname}
Version:        0.10.0
Release:        1%{?dist}
Summary:        A FIT file parsing and decoding library
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/polyvertex/fitdecode
Source0:        %{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# TODO:
# BuildRequires:  python3-sphinx
# BuildRequires:  python3-sphinx_rtd_theme

%description %{desctxt}

%package     -n python3-%{pkgname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desctxt}

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{pkgname}
%doc *.rst
%license LICENSE.txt
%{python3_sitelib}/*
%{_bindir}/*

%changelog
* Thu Dec 30 2021 Satoru SATOH <satoru.satoh@gmail.com> - 0.10.0-1
- Initial packaging
