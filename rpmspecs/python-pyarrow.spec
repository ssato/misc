%global pkgname pyarrow
%global desc \
Apache Arrow is a cross-language development platform for in-memory data. \
It specifies a standardized language-independent columnar memory format for \
flat and hierarchical data, organized for efficient analytic operations on \
modern hardware. \
\
This package provides python support for Aapche Arrow.

Name:           python-%{pkgname}
Version:        0.17.0
Release:        1%{?dist}
Summary:        Apache Arrow support for python
License:        ASL 2.0
URL:            https://pypi.org/project/pyarrow/
Source0:        %{pkgname}-%{version}.tar.gz

BuildRequires:  python3-Cython
BuildRequires:  python3-numpy
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm

%description    %{desc}

%package -n python3-%{pkgname}
Summary:        %{summary}
BuildRequires:  python3-numpy
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desc}

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{pkgname}
%doc README.md
%{python3_sitelib}/*

%changelog
* Wed Apr 22 2020 Satoru SATOH <satoru.satoh@gmail.com> - 0.17.0-1
- Initial packaging
