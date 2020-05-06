# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname Pyro4
%global desctxt \
Pyro enables you to build applications in which objects can talk to each other \
over the network, with minimal programming effort. You can just use normal \
Python method calls to call objects on other machines. Pyro is a pure Python \
library so it runs on many different platforms and Python versions.

Name:           python-%{pkgname}
Version:        4.80
Release:        1%{?dist}
Summary:        Library enables python objects can talk to eachother over the network
Group:          Development/Libraries
License:        MIT
URL:            http://pyro4.readthedocs.io
Source0:        %{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description %{desctxt}

%package     -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-serpent
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desctxt}

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{pkgname}
%doc README.md
%{python3_sitelib}/*
%{_bindir}/*

%changelog
* Wed May  6 2020 Satoru SATOH <satoru.satoh@gmail.com> - 4.80-1
- New upstream

* Sat Nov 16 2019 Satoru SATOH <satoru.satoh@gmail.com> - 4.77-1
- Initial packaging
