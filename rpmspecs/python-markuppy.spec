# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname markuppy
%global srcname MarkupPy

%global desctxt \
A python module to generate HTML/XML from a python program.

Name:           python-%{pkgname}
Version:        1.14
Release:        2%{?dist}
Summary:        Python module to generate HTML/XML from a python program
Group:          Development/Libraries
License:        MIT
URL:            https://tylerbakke.github.io/MarkupPy/
Source0:        %{srcname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description %{desctxt}

%package     -n python3-%{pkgname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desctxt}

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{pkgname}
%{python3_sitelib}/*

%changelog
* Fri Nov 15 2019 Satoru SATOH <satoru.satoh@gmail.com> - 1.14-2
- Fix the summary

* Fri Nov 15 2019 Satoru SATOH <satoru.satoh@gmail.com> - 1.14-1
- Initial packaging
