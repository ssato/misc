%global pkgname f5-sdk
%global srcname f5-common-python

%global desc \
This SDK implements an object model based SDK for the F5 Networks Big-IP(R) \
iControl REST interface. Users of this library can create, edit, update, and \
delete configuration objects on a BIG-IP(R).

Name:           python-%{pkgname}
Version:        3.0.21
Release:        2%{?dist}
Summary:        Python SDK for the F5 Networks Big-IP and iControl REST interface
License:        ASL 2.0
URL:            https://github.com/F5Networks/f5-common-python
#Source0:        %%{url}/archive/RELEASE_%%{version}.tar.gz
Source0:        %{srcname}-%{version}.tar.gz
BuildArch:      noarch

%description    %{desc}

%package -n     python3-%{pkgname}
Summary:        %{summary}
Requires:       PyYAML
Requires:       python3-six
Requires:       python3-f5-icontrol-rest
Requires:       python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python3-%{pkgname} %{desc}

%prep
%autosetup -n %{srcname}-%{version}

# avoid to install setup_requirements.txt into /usr.
sed -i.save '/data_files/d' setup.py

%build
%py3_build

%install
%py3_install

%files -n       python3-%{pkgname}
%doc README.rst
%{python3_sitelib}/*

%changelog
* Wed May  6 2020 Satoru SATOH <satoru.satoh@gmail.com> - 3.0.21-2
- Drop py2 support

* Sun Oct 13 2019 Satoru SATOH <satoru.satoh@gmail.com> - 3.0.21-1
- New upstream
- Add py3 sub package and make py2 sub package optional

* Mon Aug  6 2018 Satoru SATOH <ssato@redhat.com> - 3.0.19-1
- New upstream

* Tue Jul 31 2018 Satoru SATOH <ssato@redhat.com> - 3.0.18-1
- Initial packaging
