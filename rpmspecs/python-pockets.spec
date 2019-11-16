# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname pockets
%global desctxt \
The Pockets library pulls together many of the Python helper functions \
I’ve found useful over the years.

Name:           python-%{pkgname}
Version:        0.9.1
Release:        1%{?dist}
Summary:        Library provides many of the python helper functions
Group:          Development/Libraries
License:        BSD
URL:            https://github.com/RobRuana/pockets
Source0:        %{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description %{desctxt}

%package     -n python3-%{pkgname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desctxt}

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{pkgname}
%doc README.rst AUTHORS CHANGES
%{python3_sitelib}/*

%changelog
* Sat Nov 16 2019 Satoru SATOH <satoru.satoh@gmail.com> - 0.9.1-1
- Initial packaging
