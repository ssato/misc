%global pkgname fortiosapi
%global desc \
Python library to interact with configuration of Fortigate/Fortios devices via \
REST API and ssh.

Name:           python-%{pkgname}
Version:        1.0.1
Release:        1%{?dist}
Summary:        Python library to interact with Fortigate/Fortios devices
License:        ASL 2.0
URL:            https://github.com/fortinet-solutions-cse/fortiosapi
#Source0:        %%{url}/archive/RELEASE_%%{version}.tar.gz
Source0:        %{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description    %{desc}

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

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n         python3-%{pkgname}
%doc README.md HACKING.md
%license LICENSE
%{python3_sitelib}/*

%changelog
* Wed May  6 2020 Satoru SATOH <satoru.satoh@gmail.com> - 1.0.1-1
- New upstream
- Drop py2 support

* Thu Dec  6 2018 Satoru SATOH <ssato@redhat.com> - 0.9.91-1
- Initial packaging
