%global pkgname cfgv
%global desctxt \
Validate configuration and produce human readable error messages.

Name:           python-%{pkgname}
Version:        2.0.1
Release:        2%{?dist}
Summary:        Python library to validate configuration files
License:        MIT
URL:            https://github.com/asottile/cfgv
Source0:        %{url}/archive/RELEASE_%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description   %desctxt

%package     -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-six
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desctxt}

%prep
%autosetup -n %{pkgname}-%{version} -p1

%build
%py3_build

%install
%py3_install

%files -n python3-%{pkgname}
%doc README.md
%{python3_sitelib}/*

%changelog
* Sun Sep 29 2019 Satoru SATOH <satoru.satoh@gmail.com> - 1.2.2-2
- fix summary text

* Sun Sep 29 2019 Satoru SATOH <satoru.satoh@gmail.com> - 2.0.1-1
- Initial packaging
