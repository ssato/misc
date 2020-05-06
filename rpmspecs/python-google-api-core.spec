# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname google-api-core
%global desctxt \
This package provides a stable APIs for Google Cloud Platform.

Name:           python-%{pkgname}
Version:        1.17.0
Release:        1%{?dist}
Summary:        Python library to provides APIs for Google Cloud Platform
Group:          Development/Libraries
License:        ASL 2.0
URL:            https://github.com/googleapis/google-auth-library-python
Source0:        %{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description %{desctxt}

%package     -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-google-auth
Requires:       python3-googleapis-common-protos
Requires:       python3-grpcio
Requires:       python3-grpcio-gcp
Requires:       python3-protobuf
Requires:       python3-pytz
Requires:       python3-requests
Requires:       python3-setuptools
Requires:       python3-six
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
* Wed May  6 2020 Satoru SATOH <satoru.satoh@gmail.com> - 1.17.0-1
- Initial packaging
