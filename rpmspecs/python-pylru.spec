# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname pylru
%global srcname pylru
%global sumtxt  A LRU cache for python
%global with_python3 0

Name:           python-%{pkgname}
Version:        1.0.9
Release:        1%{?dist}
Summary:        %{sumtxt}
Group:          Development/Libraries
License:        GPLv2
#URL:            https://github.com/jlhutch/%{srcname}
URL:            https://pypi.python.org/packages/source/p/pylru/%{pkgname}-%{version}.tar.gz
Source0:        %{srcname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel python3-devel
BuildRequires:  python-setuptools python3-setuptools

%description
Pylru implements a true LRU cache along with several support classes. The cache
is efficient and written in pure Python. Basic operations (lookup, insert,
delete) all run in a constant amount of time. Pylru provides a cache class with
a simple dict interface. It also provides classes to wrap any object that has a
dict interface with a cache. Both write-through and write-back semantics are
supported. Pylru also provides classes to wrap functions in a similar way,
including a function decorator.

%package     -n python2-%{pkgname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{pkgname}
Pylru implements a true LRU cache along with several support classes. The cache
is efficient and written in pure Python. Basic operations (lookup, insert,
delete) all run in a constant amount of time. Pylru provides a cache class with
a simple dict interface. It also provides classes to wrap any object that has a
dict interface with a cache. Both write-through and write-back semantics are
supported. Pylru also provides classes to wrap functions in a similar way,
including a function decorator.

%package     -n python3-%{pkgname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{pkgname}
Pylru implements a true LRU cache along with several support classes. The cache
is efficient and written in pure Python. Basic operations (lookup, insert,
delete) all run in a constant amount of time. Pylru provides a cache class with
a simple dict interface. It also provides classes to wrap any object that has a
dict interface with a cache. Both write-through and write-back semantics are
supported. Pylru also provides classes to wrap functions in a similar way,
including a function decorator.

%prep
%setup -qn %{srcname}-%{version}

%build
%py3_build
%py2_build

%install
%py3_install
%py2_install

%files -n python2-%{pkgname}
%doc README.txt
%{python2_sitelib}/*

%files -n python3-%{pkgname}
%doc README.txt
%{python3_sitelib}/*

%changelog
* Thu Feb  4 2016 Satoru SATOH <ssato@redhat.com> - 1.0.9-1
- Initial packaging
