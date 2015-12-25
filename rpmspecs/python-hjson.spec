# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname hjson
%global sumtxt  JSON for Humans, allows comments and is less error prone
%global desctxt Hjson, the Human JSON. A data format that caters to humans and helps reduce the errors they make. It supports \#, // and /**/ style comments as well as avoiding trailing/missing comma and other mistakes. For details and syntax see hjson.org.

Name:           python-%{pkgname}
Version:        1.5.2
Release:        1%{?dist}
Summary:        %{sumtxt}
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/laktak/%{pkgname}-py
Source0:        %{pkgname}-%{version}.zip
BuildArch:      noarch
BuildRequires:  python2-devel python3-devel
BuildRequires:  python-setuptools python3-setuptools

%description
%{desctxt}

%package     -n python2-%{pkgname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname}
%{desctxt}

%package     -n python3-%{pkgname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname}
%{desctxt}

%prep
%setup -q -n %{pkgname}-%{version}

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
* Fri Dec 25 2015 Satoru SATOH <ssato@redhat.com> - 1.5.2-1
- Initial packaging
