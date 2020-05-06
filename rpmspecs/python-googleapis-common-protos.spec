# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname googleapis-common-protos
%global desctxt \
googleapis-common-protos contains the python classes generated from the \
common protos in the googleapis repository.

Name:           python-%{pkgname}
Version:        1.51.0
Release:        1%{?dist}
Summary:        Python classes generated from the common protos in the googleapis repository
Group:          Development/Libraries
License:        ASL 2.0
URL:            https://github.com/googleapis/googleapis
Source0:        %{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description %{desctxt}

%package     -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-protobuf
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
* Wed May  6 2020 Satoru SATOH <satoru.satoh@gmail.com> - 1.51.0-1
- Initial packaging
