%global pypi_name Flask-Uploads
%global pkg_name flask-uploads
%global desc \
Flask-Uploads provides flexible upload handling for Flask applications. \
It lets you divide your uploads into sets that the application user can \
publish separately.

Name:           python-%{pkg_name}
Version:        0.2.1
Release:        2%{?dist}
Summary:        Flexible and efficient upload handling for Flask
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/maxcountryman/flask-uploads
Source0:        https://pypi.python.org/packages/source/F/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-flask
BuildRequires:  python3-nose
# check can't work with python3 until builds for python3-flask-babel are available
#BuildRequires:  python3-flask-babel

%description    %{desc}

%package     -n python3-%{pkg_name}
Summary:        %{summary}
Requires:       python3-flask
%{?python_provide:%python_provide python3-%{pkg_name}}

%description -n python3-%{pkg_name} %{desc}

%prep
%autosetup -n %{pypi_name}-%{version}

cat << EOF > README.Fedora
- home: https://github.com/maxcountryman/flask-uploads
- PyPI: https://pypi.org/project/Flask-Uploads/
- doc: https://flask-uploads.readthedocs.io
EOF

%build
%py3_build

%install
%py3_install
 
%files -n python3-%{pkg_name}
%doc README.Fedora
%{python3_sitelib}/*

%changelog
* Thu May  7 2020 Satoru SATOH <satoru.satoh@gmail.com> - 0.2.1-2
- Cleanup this RPM SPEC

* Tue Feb  4 2020 Satoru SATOH <satoru.satoh@gmail.com> - 0.2.1-1
- New upstream

* Sun Sep 20 2015 Satoru SATOH <ssato@redhat.com> - 0.1.3-1
- Initial RPM release
