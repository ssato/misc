# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname serpent
%global desctxt \
Serpent is a simple serialization library based on ast.literal_eval. \
\
Because it only serializes literals and recreates the objects using \
ast.literal_eval(), the serialized data is safe to transport to other \
machines (over the network for instance) and de-serialize it there.

Name:           python-%{pkgname}
Version:        1.30.2
Release:        1%{?dist}
Summary:        A simple serialization library based on ast.literal_eval
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/irmen/Serpent
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
%doc README.md
%license LICENSE
%{python3_sitelib}/*

%changelog
* Wed May  6 2020 Satoru SATOH <satoru.satoh@gmail.com> - 1.30.2-1
- New upstream

* Sat Nov 16 2019 Satoru SATOH <satoru.satoh@gmail.com> - 1.28-1
- Initial packaging
