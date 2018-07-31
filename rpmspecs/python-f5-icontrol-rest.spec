%global pkgname f5-icontrol-rest

%global desc \
Generic python library used by the F5 SDK and other F5 projects to communicate \
with BIG-IP(R) via the REST API.

Name:           python-%{pkgname}
Version:        1.3.10
Release:        1%{?dist}
Summary:        Python library to communicate with F5 Big-IP REST API
License:        ASL 2.0
URL:            https://github.com/F5Networks/f5-icontrol-rest-python
Source0:        %{url}/archive/RELEASE_%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools

%description    %{desc}

%package -n     python2-%{pkgname}
Summary:        %{summary}
Requires:       PyYAML
Requires:       python2-six
Requires:       python2-requests
Requires:       python2-setuptools
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname} %{desc}

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py2_build

%install
%py2_install

%files -n       python2-%{pkgname}
%doc README.rst
%if 0%{?rhel} == 7
%{python_sitelib}/*
%else
%{python2_sitelib}/*
%endif

%changelog
* Tue Jul 31 2018 Satoru SATOH <ssato@redhat.com> - 1.3.10-1
- Initial packaging
