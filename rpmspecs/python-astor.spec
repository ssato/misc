%global pkgname astor
%global desc \
astor is designed to allow easy manipulation of Python source via the AST.

%bcond_with tests

Name:           python-%{pkgname}
Version:        0.8.1
Release:        1%{?dist}
Summary:        Library to read, rewrite and write python ASTs
License:        BSD
URL:            https://github.com/berkerpeksag/astor
Source0: %{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
# doc
BuildRequires:  make
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx_rtd_theme
%if %{with tests}
BuildRequires:  python3-nose
BuildRequires:  python3-flake8
BuildRequires:  python3-coverage
%endif

%description    %{desc}

%package -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-setuptools
#Requires:       python3-wheel
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desc}

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py3_build
make -C docs/ html

%install
%py3_install

%if %{with tests}
%check
tox -e py$(python -c "import sys; sys.stdout.write(sys.version[:3].replace('.', ''))")
%endif

%files -n python3-%{pkgname}
%doc AUTHORS README.rst docs/_build/html/
%license LICENSE
%{python3_sitelib}/*

%changelog
* Mon Jun 15 2020 Satoru SATOH <satoru.satoh@gmail.com> - 0.8.1-1
- Initial packaging
