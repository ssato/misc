# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname registry
%global srcname python-registry
%global with_python3 1
%global sumtxt  Read access to Windows Registry files from python
%global desctxt python-registry is a pure Python library that provides read-only access to Windows Registry files. These include NTUSER.DAT, userdiff, and SAM. The interface is two-fold: a high-level interface suitable for most tasks, and a low level set of parsing objects and methods which may be used for advanced study of the Windows Registry. The library is portable across all major platforms.

Name:           python-%{pkgname}
Version:        1.2.0
Release:        1%{?dist}
Summary:        %{sumtxt}
Group:          Development/Libraries
License:        ASL 2.0
URL:            https://github.com/williballenthin/%{srcname}
#URL:            https://pypi.python.org/packages/source/p/pylru/%{pkgname}-%{version}.tar.gz
#Source0:        %{srcname}-%{version}.tar.gz
#Source0:        https://github.com/williballenthin/%{srcname}/archive/master.zip
Source0:        %{srcname}-master.zip
BuildArch:      noarch
BuildRequires:  python2-devel python3-devel
BuildRequires:  python-setuptools python3-setuptools

%description
%{desctxt}

%package     -n python2-%{pkgname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{pkgname}
%{desctxt}

%package     -n python3-%{pkgname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{pkgname}
%{desctxt}

%prep
%setup -qn %{srcname}-master

%build
%py3_build
%py2_build

%install
%py3_install
%py2_install

%files -n python2-%{pkgname}
%doc README.MD CHANGELOG.TXT CONTRIBUTORS.TXT
%{python2_sitelib}/*

%files -n python3-%{pkgname}
%doc README.MD CHANGELOG.TXT CONTRIBUTORS.TXT
%{python3_sitelib}/*

%changelog
* Fri Jul  1 2016 Satoru SATOH <ssato@redhat.com> - 1.2.0-1
- Initial packaging
