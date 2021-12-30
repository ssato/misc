# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname iniconfig
%global desctxt \
iniconfig is a small and simple INI-file parser module having a unique set \
of features.

Name:           python-%{pkgname}
Version:        1.0.1
Release:        1%{?dist}
Summary:        A small and simple INI-file parser for python
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/RonnyPfannschmidt/iniconfig
Source0:        %{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

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
%doc CHANGELOG README.txt example.ini test_iniconfig.py
%license LICENSE
%{python3_sitelib}/*

%changelog
* Sat Sep  5 2020 Satoru SATOH <satoru.satoh@gmail.com> - 1.0.1-1
- Initial packaging
