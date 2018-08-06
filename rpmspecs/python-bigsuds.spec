%global pkgname bigsuds

%global desc \
Python library for F5 Networks iControl API

%bcond_with optionals
%bcond_with tests

%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-%{pkgname}
Version:        1.0.6
Release:        2%{?dist}
Summary:        Python library for F5 Networks iControl API
# PyPI page says EULA is required but github page says its license is MIT.
License:        MIT
URL:            https://github.com/F5Networks/bigsuds
Source0:        %{url}/archive/RELEASE_%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description    %{desc}

%package -n     python2-%{pkgname}
Summary:        %{summary}
Requires:       python2-suds
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname} %{desc}

%if %{with python3}
%package -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-suds
Requires:       python3-setuptools
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desc}
%endif

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py2_build

%if %{with python3}
%py3_build
%endif

%install
%py2_install
%if %{with python3}
%py3_install
%endif

%files -n        python2-%{pkgname}
%doc README.md
%if 0%{?rhel} == 7
%{python_sitelib}/*
%else
%{python2_sitelib}/*
%endif

%if %{with python3}
%files -n         python3-%{pkgname}
%doc README.md
%{python3_sitelib}/*
%endif

%changelog
* Mon Aug  6 2018 Satoru SATOH <ssato@redhat.com> - 1.0.6-2
- Fix license

* Tue Jul 31 2018 Satoru SATOH <ssato@redhat.com> - 1.0.6-1
- Initial packaging
