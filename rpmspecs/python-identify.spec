%global pkgname identify
%global desctxt \
File identification library for Python. \
\
Given a file (or some information about a file), return a set of \
standardized tags identifying what the file is.

Name:           python-%{pkgname}
Version:        1.4.7
Release:        2%{?dist}
Summary:        File identification library for python
License:        MIT
URL:            https://github.com/chriskuehl/identify
Source0:        %{url}/archive/RELEASE_%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description   %desctxt

%package     -n python3-%{pkgname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desctxt}

%prep
%autosetup -n %{pkgname}-%{version} -p1

%build
%py3_build

%install
%py3_install

%files -n python3-%{pkgname}
%doc README.md
%{python3_sitelib}/*
%{_bindir}/*

%changelog
* Sun Sep 29 2019 Satoru SATOH <satoru.satoh@gmail.com> - 1.4.7-1
- Initial packaging
