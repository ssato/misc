%global pkgname base58
%global desc \
Base58 and Base58Check implementation compatible with what is used by the \
bitcoin network.

%bcond_with tests

Name:           python-%{pkgname}
Version:        2.0.1
Release:        1%{?dist}
Summary:        Library to encode and decode base58 used by the bitcoin network
License:        MIT
URL:            https://github.com/keis/base58/
Source0: %{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
# .. todo::
%if %{with tests}
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-flake8
BuildRequires:  python3-cov
BuildRequires:  python3-cov
BuildRequires:  python3-PyHamcrest
BuildRequires:  python3-coveralls
%endif

%description    %{desc}

%package -n python3-%{pkgname}
Summary:        %{summary}
#Requires:       python3-wheel
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desc}

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py3_build

%install
%py3_install

%if %{with tests}
%check
tox -e py$(python -c "import sys; sys.stdout.write(sys.version[:3].replace('.', ''))")
%endif

%files -n python3-%{pkgname}
%doc *.md
%license COPYING
%{python3_sitelib}/*
%{_bindir}/*

%changelog
* Mon Jun 15 2020 Satoru SATOH <satoru.satoh@gmail.com> - 2.0.1-1
- Initial packaging
