# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname flask-bootstrap
%global pypi_name Flask-Bootstrap
%global sumtxt  Flask extension to include Bootstrap in your project
%global desctxt \
Flask-Bootstrap packages Bootstrap into an extension that mostly consists of \
a blueprint named "bootstrap" It can also create links to serve Bootstrap \
from a CDN and works with no boilerplate code in your application.

Name:           python-%{pkgname}
Version:        3.3.7.0
Release:        1%{?dist}
Summary:        %{sumtxt}
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/mbr/flask-bootstrap
Source0:        https://pypi.python.org/packages/source/F/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description    %{desctxt}

%package     -n python3-%{pkgname}
Summary:        %{sumtxt}
Requires:       python3-flask
Requires:       python3-dominate
Requires:       python3-visitor
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pkgname} %{desctxt}

%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{pkgname}
%doc README.rst
%{python3_sitelib}/*

%changelog
* Thu May  7 2020 Satoru SATOH <satoru.satoh@gmail.com> - 3.3.7.1-1
- New upstream release
- drop py2 support

* Tue Nov 22 2016 Satoru SATOH <ssato@redhat.com> - 3.3.7.0-1
- New upstream release

* Tue Sep 29 2015 Satoru SATOH <ssato@redhat.com> - 3.3.5.6-1
- Initial packaging
