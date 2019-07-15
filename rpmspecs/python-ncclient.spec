# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname ncclient
%global srcname ncclient
%global desctxt \
ncclient is a Python library that facilitates client-side scripting \
and application development around the NETCONF protocol

Name:           python-%{pkgname}
Version:        0.6.6
Release:        1%{?dist}
Summary:        Python library for NETCONF clients
Group:          Development/Libraries
License:        ASL 2.0
URL:            https://github.com/ncclient/ncclient
Source0:        %{srcname}-%{version}.tar.gz
# TODO:
# Patch10:        ncclient-0.6.6-readme-md.patch
BuildArch:      noarch

%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without python3
%bcond_with python2
%else
%bcond_with python3
%endif

%if %{with python2}
%if 0%{?rhel} == 7
BuildRequires:  python-devel
BuildRequires:  python-setuptools
%else
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%endif
%endif
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description    %{desctxt}

%if %{with python2}
%package     -n python2-%{pkgname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname} %{desctxt}
%endif

%if %{with python3}
%package     -n python3-%{pkgname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desctxt}
%endif

%prep
%autosetup -n %{srcname}-%{version}

%build
%if %{with python2}
%py2_build
%endif
%if %{with python3}
%py3_build
%endif

%install
%if %{with python2}
%py2_install
%endif
%if %{with python3}
%py3_install
%endif

%if %{with python2}
%files -n python2-%{pkgname}
%doc README*
%doc docs examples
%if 0%{?rhel} == 7
%{python_sitelib}/*
%else
%{python2_sitelib}/*
%endif
%endif

%if %{with python3}
%files -n python3-%{pkgname}
%doc README*
%doc docs examples
%{python3_sitelib}/*
%endif

%changelog
* Mon Jul 15 2019 Satoru SATOH <ssato@redhat.com> - 0.6.6-1
- Initial packaging
