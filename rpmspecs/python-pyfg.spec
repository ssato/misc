%global pkgname pyfg

%global desc \
Python API library for FortiOS or how to turn FortiOS into JunOS

%bcond_with optionals
%bcond_with tests

%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-%{pkgname}
Version:        0.50
Release:        2%{?dist}
Summary:        Python API library for FortiOS
License:        ASL 2.0
URL:            https://github.com/spotify/pyfg
Source0:        %{url}/archive/RELEASE_%{version}.tar.gz
BuildArch:      noarch
Patch0:         0001-enhancement-add-support-to-configure-channel-timeout.patch

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pip
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip
%endif

%description    %{desc}

%package -n     python2-%{pkgname}
Summary:        %{summary}
Requires:       python2-paramiko
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname} %{desc}

%if %{with python3}
%package -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-paramiko
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desc}
%endif

%prep
%autosetup -n %{pkgname}-%{version} -p1

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
%license LICENSE
%if 0%{?rhel} == 7
%{python_sitelib}/*
%else
%{python2_sitelib}/*
%endif

%if %{with python3}
%files -n         python3-%{pkgname}
%doc README.md
%license LICENSE
%{python3_sitelib}/*
%endif

%changelog
* Wed Sep 26 2018 Satoru SATOH <ssato@redhat.com> - 0.50-2
- Apply a custom patch to allow configuration of channel timeout

* Mon Aug  6 2018 Satoru SATOH <ssato@redhat.com> - 0.50-1
- Initial packaging
