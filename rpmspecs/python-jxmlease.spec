# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname jxmlease
%global srcname jxmlease
%global desctxt \
A Python module for converting XML to intelligent Python data structures, \
and converting Python data structures to XML

Name:           python-%{pkgname}
Version:        1.0.1
Release:        3%{?dist}
Summary:        Python library converting XML from/to python objects
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/Juniper/jxmlease
Source0:        %{srcname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description    %{desctxt}

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
%doc README.rst
%doc docs
%{python3_sitelib}/*

%changelog
* Wed May  6 2020 Satoru SATOH <satoru.satoh@gmail.com> - 1.0.1-3
- new upstream
- drop py2 support

* Tue Jul 16 2019 Satoru SATOH <ssato@redhat.com> - 1.0.1-2
- fix: s/sumtxt/summary/g
- disable python2 and enable python3 builds by default

* Mon Jul 15 2019 Satoru SATOH <ssato@redhat.com> - 1.0.1-1
- Initial packaging
