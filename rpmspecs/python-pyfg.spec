%global pkgname pyfg

%global desc \
Python API library for FortiOS or how to turn FortiOS into JunOS

%bcond_with optionals
%bcond_with tests

Name:           python-%{pkgname}
Version:        0.50
Release:        3%{?dist}
Summary:        Python API library for FortiOS
License:        ASL 2.0
URL:            https://github.com/spotify/pyfg
#Source0:        %{url}/archive/RELEASE_%{version}.tar.gz
Source0:        %pkgname}-%{version}.tar.gz
BuildArch:      noarch
Patch0:         0001-enhancement-add-support-to-configure-channel-timeout.patch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip

%description    %{desc}

%package -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-paramiko
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desc}

%prep
%autosetup -n %{pkgname}-%{version} -p1

%build
%py3_build

%install
%py3_install

%files -n         python3-%{pkgname}
%doc README.md
%license LICENSE
%{python3_sitelib}/*

%changelog
* Wed May  6 2020 Satoru SATOH <satoru.satoh@gmail.com> - 0.50-3
- Rebuild
- Drop py2 support

* Wed Sep 26 2018 Satoru SATOH <ssato@redhat.com> - 0.50-2
- Apply a custom patch to allow configuration of channel timeout

* Mon Aug  6 2018 Satoru SATOH <ssato@redhat.com> - 0.50-1
- Initial packaging
