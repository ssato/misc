# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname ncclient
%global srcname ncclient
%global desctxt \
ncclient is a Python library that facilitates client-side scripting \
and application development around the NETCONF protocol

Name:           python-%{pkgname}
Version:        0.6.6
Release:        2%{?dist}
Summary:        Python library for NETCONF clients
Group:          Development/Libraries
License:        ASL 2.0
URL:            https://github.com/ncclient/ncclient
Source0:        %{srcname}-%{version}.tar.gz
# TODO:
# Patch10:        ncclient-0.6.6-readme-md.patch
BuildArch:      noarch

%if 0%{?rhel} == 7 || 0%{?epel} == 7
%bcond_without python2
%else
%bcond_with python2
%endif

%if %{with python2}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
Requires:       python2-paramiko
Requires:       python2-lxml
Requires:       python2-six
%endif
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3-paramiko
Requires:       python3-lxml
Requires:       python3-six

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
%files -n python2-%{pkgname}
%doc README*
%doc docs examples
%{python2_sitelib}/*
%endif

%files -n python3-%{pkgname}
%doc README*
%doc docs examples
%{python3_sitelib}/*

%changelog
* Tue Jul 16 2019 Satoru SATOH <ssato@redhat.com> - 1.0.1-2
- fix: s/sumtxt/summary/g
- disable python2 and enable python3 builds by default

* Mon Jul 15 2019 Satoru SATOH <ssato@redhat.com> - 0.6.6-1
- Initial packaging
