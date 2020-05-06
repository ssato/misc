%global pkgname testfixtures
%global desc \
Testfixtures is a collection of helpers and mock objects that are useful \
when writing automated tests in Python.

%bcond_with doc

Name:           python-%{pkgname}
Version:        6.14.1
Release:        1%{?dist}
Summary:        A collection of helpers and mock objects for python
License:        MIT
URL:            https://github.com/Simplistix/testfixtures
Source0:        https://pypi.python.org/packages/source/t/%{pkgname}/%{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with doc}
BuildRequires:  python3-sphinx
BuildRequires:  python3-mock
BuildRequires:  python3-python-zope-component
BuildRequires:  python3-django
BuildRequires:  python3-sybil
BuildRequires:  python3-twisted
%endif

%description    %{desc}

%package -n python3-%{pkgname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desc}

%if %{with doc}
%package -n python3-%{pkgname}-doc
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pkgname}-doc}

%description -n python3-%{pkgname}-doc %{desc}
%endif

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n         python3-%{pkgname}
%doc *.rst
%license LICENSE.txt
%{python3_sitelib}/*

%changelog
* Thu May  7 2020 Satoru SATOH <satoru.satoh@gmail.com> - 6.14.1-1
- Initial packaging
