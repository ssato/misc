%define mod_name pylint-flask

Name:           python3-pylint-flask
Version:        0.6
Release:        1%{?dist}
Summary:        Pylint plugin to analyze Flask applications
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/jschaf/pylint-flask
# TODO:
# Source0:        http://pypi.python.org/packages/source/...
Source0:        %{mod_name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3-pylint

%description
Pylint plugin to analyze Flask applications.

%prep
%autosetup -n %{mod_name}-%{version}

%build
%py3_build

cat << EOF > README.Fedora
%{description}

- https://github.com/jschaf/pylint-flask
EOF

%install
%py3_install
 
%files
%doc README.Fedora
%{python3_sitelib}/*

%changelog
* Tue Mar 24 2020 Satoru SATOH <satoru.satoh@gmail.com> - 0.6-1
- Initial RPM release
