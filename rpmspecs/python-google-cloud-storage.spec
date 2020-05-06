# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname google-cloud-storage
%global desctxt \
Google Cloud Storage allows you to store data on Google infrastructure with \
very high reliability, performance and availability, and can be used to \
distribute large data objects to users via direct download.

Name:           python-%{pkgname}
Version:        1.28.1
Release:        1%{?dist}
Summary:        Python library to store data on Google Cloud Platform
Group:          Development/Libraries
License:        ASL 2.0
URL:            https://github.com/googleapis/python-storage
Source0:        %{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description %{desctxt}

%package     -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-google-auth
Requires:       python3-google-cloud-core
Requires:       python3-google-resumable-media
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
%{python3_sitelib}/*

%changelog
* Wed May  6 2020 Satoru SATOH <satoru.satoh@gmail.com> - 1.28.1-1
- Initial packaging
