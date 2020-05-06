# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname google-cloud-core
%global desctxt \
The google-cloud-core package contains helpers common to all google-cloud-*\
packages. In an attempt to reach a stable API, much of the functionality \
has been split out into a new package google-api-core.

Name:           python-%{pkgname}
Version:        1.3.0
Release:        1%{?dist}
Summary:        Library contains helpers common to all google-cloud-* pakcages
Group:          Development/Libraries
License:        ASL 2.0
URL:            https://github.com/GoogleCloudPlatform/google-cloud-python
Source0:        %{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description %{desctxt}

%package     -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-google-api-core
Requires:       python3-grpcio
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desctxt}

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{pkgname}
%doc README.rst
%license LICENSE
%{python3_sitelib}/*

%changelog
* Wed May  6 2020 Satoru SATOH <satoru.satoh@gmail.com> - 1.3.0-1
- Initial packaging
