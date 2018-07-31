%global pkgname f5-sdk

%global desc \
This SDK implements an object model based SDK for the F5 Networks Big-IP(R) \
iControl(R) REST interface. Users of this library can create, edit, update, and \
delete configuration objects on a BIG-IP(R).

Name:           python-%{pkgname}
Version:        3.0.18
Release:        1%{?dist}
Summary:        Python SDK for the F5 Networks Big-IP and iControl REST interface
License:        ASL 2.0
URL:            https://github.com/F5Networks/f5-common-python
Source0:        %{url}/archive/RELEASE_%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools

%description    %{desc}

%package -n     python2-%{pkgname}
Summary:        %{summary}
Requires:       PyYAML
Requires:       python2-six
Requires:       python2-f5-icontrol-rest
Requires:       python2-setuptools
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname} %{desc}

%prep
%autosetup -n %{pkgname}-%{version}

# avoid to install setup_requirements.txt into /usr.
sed -i.save '/data_files/d' setup.py

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
* Tue Jul 31 2018 Satoru SATOH <ssato@redhat.com> - 3.0.18-1
- Initial packaging
