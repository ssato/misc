# .. seealso:: https://fedoraproject.org/wiki/Packaging:Python
%global pkgname tqdm
%global desctxt \
tqdm means "progress" in Arabic (taqadum, تقدّم) and is an abbreviation for "\
I love you so much" in Spanish (te quiero demasiado).  Instantly make your \
loops show a smart progress meter - just wrap any iterable with tqdm(iterable), \
and you're done!

Name:           python-%{pkgname}
Version:        4.28.0
Release:        1%{?dist}
Summary:        A fast, extensible progress bar for Python and CLI
License:        MIT
URL:            https://github.com/tqdm/tqdm
Source0:        %{pkgname}-%{version}.tar.gz
BuildArch:      noarch

%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without python3
%else
%bcond_with python3
%endif

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description    %{desctxt}

%package        -n python2-%{pkgname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pkgname}}

%description    -n python2-%{pkgname} %{desctxt}

%if %{with python3}
%package        -n python3-%{pkgname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pkgname}}

%description    -n python3-%{pkgname} %{desctxt}
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

%files          -n python2-%{pkgname}
%doc README.rst
%if 0%{?rhel} == 7
%{python_sitelib}/*
%else
%{python2_sitelib}/*
%endif

%if %{with python3}
%files          -n python3-%{pkgname}
%doc README.rst
%{python3_sitelib}/*
%endif
%{_bindir}/*

%changelog
* Mon Oct 22 2018 Satoru SATOH <ssato@redhat.com> - 4.28.0-1
- Initial packaging
