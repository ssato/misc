%global pkgname yapf

%global desc \
Yet Another Python code Formatter like autopep8 and pep8ify.

%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-%{pkgname}
Version:        0.22.0
Release:        1%{?dist}
Summary:        Yet Another Python code Formatter
License:        ASL 2.0
URL:            https://github.com/google/yapf
Source0:        %{url}/archive/RELEASE_%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description    %{desc}

%package -n     python2-%{pkgname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname} %{desc}

%if %{with python3}
%package -n python3-%{pkgname}
Summary:        %{summary}
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

%files -n        python2-%{pkgname}
%doc AUTHORS CHANGELOG CONTRIBUTING.rst CONTRIBUTORS HACKING.rst README.rst
%license LICENSE
%if 0%{?rhel} == 7
%{python_sitelib}/*
%else
%{python2_sitelib}/*
%endif

%if %{with python3}
%files -n         python3-%{pkgname}
%doc AUTHORS CHANGELOG CONTRIBUTING.rst CONTRIBUTORS HACKING.rst README.rst
%license LICENSE
%{python3_sitelib}/*
%{python3_sitelib}/*
%endif
%{_bindir}/*

%changelog
* Fri Aug 10 2018 Satoru SATOH <ssato@redhat.com> - 0.22.0-1
- Initial packaging
