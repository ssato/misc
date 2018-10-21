# .. seealso:: https://fedoraproject.org/wiki/Packaging:Python
%global pkgname mwparserfromhell
%global desctxt \
mwparserfromhell (the MediaWiki Parser from Hell) is a Python package that \
provides an easy-to-use and outrageously powerful parser for MediaWiki \
wikicode.

Name:           python-%{pkgname}
Version:        0.5.1
Release:        1%{?dist}
Summary:        A Python parser for MediaWiki wikicode
License:        MIT
URL:            https://github.com/earwig/mwparserfromhell
Source0:        %{pkgname}-%{version}.tar.gz

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
%doc README.rst CHANGELOG
%if 0%{?rhel} == 7
%{python_sitearch}/*
%else
%{python2_sitearch}/*
%endif

%if %{with python3}
%files          -n python3-%{pkgname}
%doc README.rst CHANGELOG
%{python3_sitearch}/*
%endif

%changelog
* Mon Oct 22 2018 Satoru SATOH <ssato@redhat.com> - 0.5.1-1
- Initial packaging
