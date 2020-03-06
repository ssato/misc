%global pkgname pylint_flask_sqlalchemy

Name:           python3-%{pkgname}
Version:        0.2.0
Release:        1%{?dist}
Summary:        A pylint plugin for improving code analysis with Flask-SQLAlchemy
License:        GPLv3
Group:          Development/Languages
URL:            https://gitlab.anybox.cloud/rboyer/pylint_flask_sqlalchemy
Source0:        https://pypi.python.org/packages/source/m/%{pkgname}/%{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-astroid
BuildRequires:  python3-pytest
Requires:       python3-pylint
Requires:       python3-flask-sqlalchemy

%description
pylint_flask_sqlalchemy is a Pylint plugin for improving code analysis with
Flask-SQLAlchemy.

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py3_build

%install
%py3_install

%check
: # TODO

%files
%doc README.md
%{python3_sitelib}/*

%changelog
* Fri Mar  6 2020 Satoru SATOH <satoru.satoh@gmail.com> - 0.2.0-1
- Initial packaging
