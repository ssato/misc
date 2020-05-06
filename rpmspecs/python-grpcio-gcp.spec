# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname grpcio-gcp
%global desctxt \
gRPC extensions for Google Cloud Platform.

Name:           python-%{pkgname}
Version:        0.2.2
Release:        1%{?dist}
Summary:        Python library to provides gRPC extensions for Google Cloud Platform
Group:          Development/Libraries
License:        ASL 2.0
URL:            https://grpc.io
Source0:        %{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description %{desctxt}

%package     -n python3-%{pkgname}
Summary:        %{summary}
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
%doc *.rst
%license LICENSE
%{python3_sitelib}/*

%changelog
* Wed May  6 2020 Satoru SATOH <satoru.satoh@gmail.com> - 0.2.2-1
- Initial packaging
