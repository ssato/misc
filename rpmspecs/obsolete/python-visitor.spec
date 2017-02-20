# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global srcname visitor
%global sumtxt  A tiny pythonic visitor implementation

Name:           python-%{srcname}
Version:        0.1.2
Release:        1%{?dist}
Summary:        %{sumtxt}
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/Knio/%{srcname}
Source0:        %{srcname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel python3-devel
BuildRequires:  python-setuptools python3-setuptools

%description
A tiny library to facilitate visitor implementation in Python (which are
slightly peculiar due to dynamic typing). In fact, it is so small, you may just
be better off copy & pasting the source straight into your project.

%package     -n python2-%{srcname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
A tiny library to facilitate visitor implementation in Python (which are
slightly peculiar due to dynamic typing). In fact, it is so small, you may just
be better off copy & pasting the source straight into your project.

%package     -n python3-%{srcname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
A tiny library to facilitate visitor implementation in Python (which are
slightly peculiar due to dynamic typing). In fact, it is so small, you may just
be better off copy & pasting the source straight into your project.

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
* Tue Sep 29 2015 Satoru SATOH <ssato@redhat.com> - 0.1.2-1
- Initial packaging
