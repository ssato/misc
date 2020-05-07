%global pypi_name Flask-Testing
%global pkg_name flask-testing
%global desc \
Flask-Testing provides unit testing utilities for Flask.

Name:           python-%{pkg_name}
Version:        0.8.0
Release:        2%{?dist}
Summary:        Unittest extensions for Flask
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/jarus/flask-testing
Source0:        https://pypi.python.org/packages/source/F/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-flask
BuildRequires:  python3-sphinx

%description    %{desc}

%package     -n python3-%{pkg_name}
Summary:        %{summary}
Requires:       python3-flask
%{?python_provide:%python_provide python3-%{pkg_name}}

%description -n python3-%{pkg_name} %{desc}

%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py3_build
make -C docs html

%install
%py3_install
 
%files -n python3-%{pkg_name}
%doc README docs/_build/html/
%license LICENSE
%{python3_sitelib}/*

%changelog
* Thu May  7 2020 Satoru SATOH <satoru.satoh@gmail.com> - 0.8.0-2
- Cleanup this RPM SPEC
- Build and add HTML docs

* Sat Mar 14 2020 Satoru SATOH <satoru.satoh@redhat.com> - 0.8.0-1
- Initial RPM release
