%global pkgname f5-icontrol-rest
%global srcname f5-icontrol-rest-python

%global desc \
Generic python library used by the F5 SDK and other F5 projects to communicate \
with BIG-IP(R) via the REST API.

Name:           python-%{pkgname}
Version:        1.3.15
Release:        1%{?dist}
Summary:        Python library to communicate with F5 Big-IP REST API
License:        ASL 2.0
URL:            https://github.com/F5Networks/f5-icontrol-rest-python
#Source0:        %%{url}/archive/RELEASE_%%{version}.tar.gz
Source0:        %{srcname}-%{version}.tar.gz
BuildArch:      noarch

%description    %{desc}

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
%py3_build

%install
%py3_install

%files -n       python3-%{pkgname}
%doc README.rst *.md
%license LICENSE
%{python3_sitelib}/*

%changelog
* Wed May  6 2020 Satoru SATOH <satoru.satoh@gmail.com> - 1.3.15-1
- New upstream
- Drop py2 support

* Sun Oct 13 2019 Satoru SATOH <satoru.satoh@gmail.com> - 1.3.13-1
- New upstream
- Add py3 sub package and make py2 sub package optional

* Mon Aug  6 2018 Satoru SATOH <ssato@redhat.com> - 1.3.11-1
- New upstream

* Tue Jul 31 2018 Satoru SATOH <ssato@redhat.com> - 1.3.10-1
- Initial packaging
