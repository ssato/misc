# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname flask-bootstrap
%global srcname Flask-Bootstrap
%global sumtxt  Flask extension to include Bootstrap in your project

Name:           python-%{pkgname}
Version:        3.3.5.6
Release:        1%{?dist}
Summary:        %{sumtxt}
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/Knio/%{srcname}
Source0:        %{srcname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel python3-devel
BuildRequires:  python-setuptools python3-setuptools

%description
Flask-Bootstrap packages Bootstrap into an extension that mostly consists of a
blueprint named "bootstrap" It can also create links to serve Bootstrap from a
CDN and works with no boilerplate code in your application.

%package     -n python2-%{pkgname}
Summary:        %{sumtxt}
Requires:       python-flask
Requires:       python2-dominate
Requires:       python2-visitor
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{pkgname}
Flask-Bootstrap packages Bootstrap into an extension that mostly consists of a
blueprint named "bootstrap" It can also create links to serve Bootstrap from a
CDN and works with no boilerplate code in your application.

%package     -n python3-%{pkgname}
Summary:        %{sumtxt}
Requires:       python3-flask
Requires:       python3-dominate
Requires:       python3-visitor
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{pkgname}
Flask-Bootstrap packages Bootstrap into an extension that mostly consists of a
blueprint named "bootstrap" It can also create links to serve Bootstrap from a
CDN and works with no boilerplate code in your application.

%prep
%setup -q -n %{srcname}-%{version}

%build
%py3_build
%py2_build

%install
%py3_install
%py2_install

%files -n python2-%{pkgname}
%doc README.rst
%{python2_sitelib}/*

%files -n python3-%{pkgname}
%doc README.rst
%{python3_sitelib}/*

%changelog
* Tue Sep 29 2015 Satoru SATOH <ssato@redhat.com> - 3.3.5.6-1
- Initial packaging
