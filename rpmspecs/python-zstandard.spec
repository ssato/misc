%global pkgname zstandard
%global desc \
Zstd, short for Zstandard, is a new lossless compression algorithm, \
which provides both good compression ratio and speed for your \
standard compression needs. \
\
This package provides python bindings to zstd library.

Name:           python-%{pkgname}
Version:        0.13.0
Release:        1%{?dist}
Summary:        Python bindings to zstd library
License:        BSD
URL:            https://github.com/indygreg/python-zstandard
Source0:        %{pkgname}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  python3-cffi
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel

%description    %{desc}

%package -n python3-%{pkgname}
Summary:        %{summary}
Requires:       libzstd
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desc}

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{pkgname}
%doc README.rst
%license LICENSE
%{python3_sitearch}/*

%changelog
* Wed Apr 22 2020 Satoru SATOH <satoru.satoh@gmail.com> - 0.13.0-1
- Initial packaging
