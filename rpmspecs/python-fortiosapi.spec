%global pkgname fortiosapi
%global desc \
Python library to interact with configuration of Fortigate/Fortios devices via \
REST API and ssh.

%if 0%{?fedora} || 0%{?rhel} > 7 || 0%{?epel} > 7
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-%{pkgname}
Version:        0.9.91
Release:        1%{?dist}
Summary:        Python library to interact with Fortigate/Fortios devices
License:        ASL 2.0
URL:            https://github.com/fortinet-solutions-cse/fortiosapi
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
Requires:       python2-paramiko
Requires:       python2-requests
Requires:       python2-pexpect
Requires:       python2-pyyaml
Requires:       python2-nose
Requires:       python2-packaging
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname} %{desc}

%if %{with python3}
%package -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-paramiko
Requires:       python3-requests
Requires:       python3-pexpect
Requires:       python3-pyyaml
Requires:       python3-nose
Requires:       python3-packaging
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
%doc README.md HACKING.md examples .idea tests
%license LICENSE
%if 0%{?rhel} == 7
%{python_sitelib}/*
%else
%{python2_sitelib}/*
%endif

%if %{with python3}
%files -n         python3-%{pkgname}
%doc README.md HACKING.md examples .idea tests
%license LICENSE
%{python3_sitelib}/*
%endif

%changelog
* Thu Dec  6 2018 Satoru SATOH <ssato@redhat.com> - 0.9.91-1
- Initial packaging
