# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname amazon-ion
%global srcname amazon.ion
%global sumtxt Python library to load and dump Amazon Ion data
%global desctxt \
Amazon Ion is a richly-typed, self-describing, hierarchical data serialization\
format offering interchangeable binary and text representations. This python\
library adds support of loading and dumping Amazon Ion data.

Name:           python-%{pkgname}
Version:        0.2.0
Release:        1%{?dist}
Summary:        %{sumtxt}
Group:          Development/Libraries
License:        ASL 2.0
#URL:            https://pypi.python.org/pypi/amazon.ion/
URL:            https://github.com/amzn/ion-python
Source0:        %{srcname}-%{version}.tar.gz
BuildArch:      noarch

%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without python3
%else
%bcond_with python3
%endif

%if 0%{?rhel} == 7
BuildRequires:  python-devel
BuildRequires:  python-setuptools
%else
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%endif
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description    %{desctxt}

%package     -n python2-%{pkgname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname} %{desctxt}

%if %{with python3}
%package     -n python3-%{pkgname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desctxt}
%endif

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
%py2_build
%if %{with python3}
%py3_build
%endif

%install
%py2_install
%if %{with python3}
%py3_install
%endif

%files -n python2-%{pkgname}
%doc README.Fedora
%if 0%{?rhel} == 7
%{python_sitelib}/*
%else
%{python2_sitelib}/*
%endif

%if %{with python3}
%files -n python3-%{pkgname}
%doc README.Fedora
%{python3_sitelib}/*
%endif

%changelog
* Tue Jan  9 2018 Satoru SATOH <ssato@redhat.com> - 0.2.0-1
- Initial packaging
