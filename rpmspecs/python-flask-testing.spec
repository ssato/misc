%global mod_name Flask-Testing

Name:           python3-flask-testing
Version:        0.8.0
Release:        1%{?dist}
Summary:        Unittest extensions for Flask
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/jarus/flask-testing
# TODO:
# Source0:        http://pypi.python.org/packages/source/...
Source0:        %{mod_name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-flask

%description
Flask-Testing provides unit testing utilities for Flask.

%prep
%autosetup -n %{mod_name}-%{version}

%build
%py3_build

%install
%py3_install
 
%files
%doc README
%{python3_sitelib}/*

%changelog
* Sat Mar 14 2020 Satoru SATOH <satoru.satoh@redhat.com> - 0.8.0-1
- Initial RPM release
