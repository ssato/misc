# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global srcname dominate
%global sumtxt  Python library to create and manipulate HTML documents using DOM API

Name:           python-%{srcname}
Version:        2.1.16
Release:        1%{?dist}
Summary:        %{sumtxt}
Group:          Development/Libraries
License:        LGPLv3
URL:            https://github.com/Knio/%{srcname}
Source0:        %{srcname}-%{version}.zip
BuildArch:      noarch
BuildRequires:  python2-devel python3-devel
BuildRequires:  python-setuptools python3-setuptools

%description
Dominate is a Python library for creating and manipulating HTML documents using
an elegant DOM API. It allows you to write HTML pages in pure Python very
concisely, which eliminate the need to learn another template language, and to
take advantage of the more powerful features of Python.

%package     -n python2-%{srcname}
Summary:        %{sumtxt}
#Requires:       python-greenlet
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
Dominate is a Python library for creating and manipulating HTML documents using
an elegant DOM API. It allows you to write HTML pages in pure Python very
concisely, which eliminate the need to learn another template language, and to
take advantage of the more powerful features of Python.

%package     -n python3-%{srcname}
Summary:        %{sumtxt}
#Requires:       python3-greenlet
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
Dominate is a Python library for creating and manipulating HTML documents using
an elegant DOM API. It allows you to write HTML pages in pure Python very
concisely, which eliminate the need to learn another template language, and to
take advantage of the more powerful features of Python.

%prep
%setup -q -n %{srcname}-%{version}

%build
%py3_build
%py2_build

%install
%py3_install
%py2_install

%files -n python2-%{srcname}
%doc README.rst
%{python2_sitelib}/*

%files -n python3-%{srcname}
%doc README.rst
%{python3_sitelib}/*

%changelog
* Tue Sep 29 2015 Satoru SATOH <ssato@redhat.com> - 2.1.16-1
- Initial packaging
