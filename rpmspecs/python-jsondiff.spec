# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname jsondiff
%global desctxt \
Diff JSON and JSON-like structures in Python.

Name:           python-%{pkgname}
Version:        1.2.0
Release:        2%{?dist}
Summary:        Python library diffs JSON and JSON-like structures
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/fzumstein/jsondiff
Source0:        %{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description    %{desctxt}

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
%doc README.rst
%{python3_sitelib}/*
%{_bindir}/*diff

%changelog
* Wed May  6 2020 Satoru SATOH <satoru.satoh@gmail.com> - 1.2.0-2
- Drop py2 support

* Mon Feb 24 2020 Satoru SATOH <satoru.satoh@gmail.com> - 1.2.0-1
- Initial packaging
