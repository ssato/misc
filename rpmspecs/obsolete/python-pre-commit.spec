%global pkgname pre-commit
%global desctxt \
A framework for managing and maintaining multi-language pre-commit hooks. \
For more information see: https://pre-commit.com

Name:           python-%{pkgname}
Version:        1.18.3
Release:        1%{?dist}
Summary:        A framework for managing multi-language pre-commit hooks
License:        MIT
URL:            https://github.com/pre-commit/pre-commit/
Source0:        %{url}/archive/RELEASE_%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description   %desctxt

%package     -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-importlib-metadata
Requires:       python3-nodeenv
Requires:       python3-pyyaml
Requires:       python3-six
Requires:       python3-toml
Requires:       python3-virtualenv
# It's not in Fedora repo but available from my copr repo,
# https://copr.fedorainfracloud.org/coprs/ssato/extras/
Requires:       python3-aspy-yaml
Requires:       python3-cfgv
Requires:       python3-identify
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desctxt}

%prep
%autosetup -n %{pkgname}-%{version} -p1

%build
%py3_build

%install
%py3_install

%files -n python3-%{pkgname}
%doc *.md
%{python3_sitelib}/*
%{_bindir}/*

%changelog
* Sun Sep 29 2019 Satoru SATOH <satoru.satoh@gmail.com> - 1.18.3-1
- Initial packaging
