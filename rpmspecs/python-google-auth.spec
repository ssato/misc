# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname google-auth
%global desctxt \
This library simplifies using Google’s various server-to-server \
authentication mechanisms to access Google APIs.

Name:           python-%{pkgname}
Version:        1.14.1
Release:        1%{?dist}
Summary:        Python library to simplify Google's auth to access Google APIs
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
Requires:       python3-cachetools
Requires:       python3-pyasn1
Requires:       python3-rsa
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
* Wed May  6 2020 Satoru SATOH <satoru.satoh@gmail.com> - 1.14.1-1
- Initial packaging
