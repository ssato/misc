%global pkgname f5-icontrol-rest
%global srcname f5-icontrol-rest-python

%global desc \
Generic python library used by the F5 SDK and other F5 projects to communicate \
with BIG-IP(R) via the REST API.

%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without python2
%else
%bcond_with python2
%endif

Name:           python-%{pkgname}
Version:        1.3.13
Release:        1%{?dist}
Summary:        Python library to communicate with F5 Big-IP REST API
License:        ASL 2.0
URL:            https://github.com/F5Networks/f5-icontrol-rest-python
Source0:        %{url}/archive/RELEASE_%{version}.tar.gz
BuildArch:      noarch

%description    %{desc}

%if %{with python2}
%package -n     python2-%{pkgname}
Summary:        %{summary}
Requires:       PyYAML
Requires:       python2-six
Requires:       python2-requests
Requires:       python2-setuptools
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname} %{desc}
%endif

%package -n     python3-%{pkgname}
Summary:        %{summary}
Requires:       PyYAML
Requires:       python3-six
Requires:       python3-requests
Requires:       python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python3-%{pkgname} %{desc}

%prep
%autosetup -n %{srcname}-%{version}

%build
%if %{with python2}
%py2_build
%endif
%py3_build

%install
%if %{with python2}
%py2_install
%endif
%py3_install

%if %{with python2}
%files -n       python2-%{pkgname}
%doc README.rst
%{python2_sitelib}/*
%endif

%files -n       python3-%{pkgname}
%doc README.rst
%{python3_sitelib}/*

%changelog
* Sun Oct 13 2019 Satoru SATOH <satoru.satoh@gmail.com> - 1.3.13-1
- New upstream
- Add py3 sub package and make py2 sub package optional

* Mon Aug  6 2018 Satoru SATOH <ssato@redhat.com> - 1.3.11-1
- New upstream

* Tue Jul 31 2018 Satoru SATOH <ssato@redhat.com> - 1.3.10-1
- Initial packaging
