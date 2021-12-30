# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname doc8
%global desctxt \
An opinionated style checker for rst (with basic support for plain text) \
styles of documentation.

Name:           python-%{pkgname}
Version:        0.8.1
Release:        1%{?dist}
Summary:        An opinionated style checker for rst
Group:          Development/Libraries
License:        ASL 2.0
URL:            https://github.com/pycqa/doc8
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
%doc *.rst AUTHORS ChangeLog
%license LICENSE
%{python3_sitelib}/*

%changelog
* Fri Sep  4 2020 Satoru SATOH <satoru.satoh@gmail.com> - 0.8.1-1
- Initial packaging
