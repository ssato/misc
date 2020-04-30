# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname amazon-ion
%global srcname ion-python
%global desctxt \
Amazon Ion is a richly-typed, self-describing, hierarchical data serialization\
format offering interchangeable binary and text representations. This python\
library adds support of loading and dumping Amazon Ion data.

%bcond_without python2

Name:           python-%{pkgname}
Version:        0.6.0
Release:        1%{?dist}
Summary:        Python library to load and dump Amazon Ion data
Group:          Development/Libraries
License:        ASL 2.0
#URL:            https://pypi.python.org/pypi/amazon.ion/
URL:            https://github.com/amzn/ion-python
Source0:        %{srcname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%if %{with python2}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%endif

%description    %{desctxt}

%if %{with python2}
%package     -n python2-%{pkgname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname} %{desctxt}
%endif

%package     -n python3-%{pkgname}
Summary:        %{sum}
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desctxt}

%prep
%autosetup -n %{srcname}-%{version}

# Avoid build error later.
sed -i "/.*'pytest-runner',/d" setup.py

cat << EOF > README.Fedora
%{desctxt}

See also:

- github: https://github.com/amzn/ion-python
- Amazon Ion / doc: http://amzn.github.io/ion-docs/
EOF

%build
%if %{with python2}
%py2_build
%endif
%py3_build

%install
%if %{with python2}
%py2_install
%endif
%py3_install

%if %{with python2}
%files -n python2-%{pkgname}
%doc README.Fedora
%{python2_sitelib}/*
%endif

%files -n python3-%{pkgname}
%doc README.Fedora
%{python3_sitelib}/*

%changelog
* Thu Apr 30 2020 Satoru SATOH <satoru.satoh@gmail.com> - 0.6.0-1
- New upstream
- eanble py3 instead of py2 and do not build py2 by default

* Tue Jan  9 2018 Satoru SATOH <ssato@redhat.com> - 0.2.0-1
- Initial packaging
