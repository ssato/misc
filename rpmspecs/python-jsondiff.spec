# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname jsondiff
%global desctxt \
Diff JSON and JSON-like structures in Python.

%if 0%{?rhel} == 7 || 0%{?epel} == 7
%bcond_without python2
%else
%bcond_with python2
%endif

Name:           python-%{pkgname}
Version:        1.2.0
Release:        1%{?dist}
Summary:        Python library diffs JSON and JSON-like structures
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/fzumstein/jsondiff
Source0:        %{pkgname}-%{version}.tar.gz
BuildArch:      noarch

%if %{with python2}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%endif
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description    %{desctxt}

%if %{with python2}
%package     -n python2-%{pkgname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname} %{desctxt}
%endif

%package     -n python3-%{pkgname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desctxt}

%prep
%autosetup -n %{pkgname}-%{version}

%build
%if %{with python2}
%py2_build
%endif
%py3_build

%install
%if %{with python2}
%py2_install
# rename executables
(for x in %{buildroot}%{_bindir}/*; do mv $x-2; done)
%endif
%py3_install

%if %{with python2}
%files -n python2-%{pkgname}
%doc README.rst
%{python2_sitelib}/*
%{_bindir}/*-2
%endif

%files -n python3-%{pkgname}
%doc README.rst
%{python3_sitelib}/*
%{_bindir}/*diff

%changelog
* Mon Feb 24 2020 Satoru SATOH <satoru.satoh@gmail.com> - 1.2.0-1
- Initial packaging
