%global pkgname aspy-yaml
%global srcname aspy.yaml
%global desctxt \
Some extensions to pyyaml.

Name:           python-%{pkgname}
Version:        1.3.0
Release:        1%{?dist}
Summary:        Some extensions to pyyaml
License:        MIT
URL:            https://github.com/asottile/cfgv
Source0:        %{url}/archive/RELEASE_%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description   %desctxt

%package     -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-pyyaml
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desctxt}

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{pkgname}
%doc README.md
%{python3_sitelib}/*

%changelog
* Sun Sep 29 2019 Satoru SATOH <satoru.satoh@gmail.com> - 1.3.0-1
- Initial packaging
