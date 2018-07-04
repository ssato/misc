%global pkgname hp3parclient

%global desc \
A  Client library that can talk to the HP 3PAR Storage array which has a REST \
web service interface and a command line interface. This client library \
implements a simple interface for talking with either interface, as needed.

%bcond_with tests
%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-%{pkgname}
Version:        3.3.2
Release:        1%{?dist}
Summary:        A Python client library for HP 3PAR Storage array
License:        ASL 2.0
URL:            https://pypi.org/project/hp3parclient/
# FIXME
#Source0:        https://files.pythonhosted.org/packages/89/d1/9593368c70e89af4125ca989da6cba209872a05e5d4d58e75a2d6e397844/hp3parclient-3.3.2.tar.gz
Source0:        %{pkgname}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%if %{with tests}
BuildRequires:  python2-nose
BuildRequires:  python2-werkzeug
BuildRequires:  python2-nose-testconfig
BuildRequires:  python2-requests
%endif
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with tests}
BuildRequires:  python3-nose
BuildRequires:  python3-werkzeug
BuildRequires:  python3-nose-testconfig
BuildRequires:  python3-requests
%endif
%endif

%description    %{desc}

%package -n python2-%{pkgname}
Summary:        %{summary}
Requires:       python2-paramiko
Requires:       python2-eventlet
Requires:       python2-requests
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname} %{desc}

%if %{with python3}
%package -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python2-paramiko
Requires:       python2-eventlet
Requires:       python2-requests
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desc}
%endif

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py2_build

%if %{with python3}
%py3_build
%endif

%install
%py2_install
%if %{with python3}
%py3_install
%endif

# cleanup tests
rm -rf %{buildroot}/usr/lib/python*/site-packages/test

%if %{with tests}
%check
tox -e py27
%if %{with python3}
tox -e py36
%endif
%endif

%files -n python2-%{pkgname}
%doc README.rst
%if 0%{?rhel} == 7
%{python_sitelib}/*
%else
%{python2_sitelib}/*
%endif

%if %{with python3}
%files -n python3-%{pkgname}
%doc README.rst
%{python3_sitelib}/*
%endif

%changelog
* Wed Jul  4 2018 Satoru SATOH <ssato@redhat.com> - 3.3.2-1
- Initial packaging
