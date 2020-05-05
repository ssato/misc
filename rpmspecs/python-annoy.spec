# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname annoy
%global desctxt \
Annoy (Approximate Nearest Neighbors Oh Yeah) is a C++ library with Python \
bindings to search for points in space that are close to a given query point. \
It also creates large read-only file-based data structures that are mmapped \
into memory so that many processes may share the same data.

Name:           python-%{pkgname}
Version:        1.16.3
Release:        1%{?dist}
Summary:        Approximate Nearest Neighbors in C++/Python optimized for memory usage
Group:          Development/Libraries
License:        ASL 2.0
URL:            https://github.com/spotify/annoy
Source0:        %{pkgname}-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-nose
BuildRequires:  gcc-c++

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
%doc README* RELEASE* examples
%{python3_sitearch}/*

%changelog
* Tue May  5 2020 Satoru SATOH <satoru.satoh@gmail.com> - 1.16.3-1
- New upstream release
- Add some more documents, examples/, etc.

* Sat Nov 16 2019 Satoru SATOH <satoru.satoh@gmail.com> - 1.16.2-1
- Initial packaging
