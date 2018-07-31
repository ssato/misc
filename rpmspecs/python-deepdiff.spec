%global pkgname deepdiff

%global desc \
Deep Difference of dictionaries, iterables, strings and other objects. It \
will recursively look for all the changes.

%bcond_with tests

%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-%{pkgname}
Version:        3.3.0
Release:        1%{?dist}
Summary:        Deep Difference and Search of any Python object/data
License:        MIT
URL:            https://github.com/seperman/deepdiff/
Source0:        %{url}/archive/RELEASE_%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%if %{with tests}
BuildRequires:  python2-mock
%endif
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with tests}
BuildRequires:  python3-mock
%endif
%endif

%description    %{desc}

%package -n     python2-%{pkgname}
Summary:        %{summary}
# Maybe EPEL is required.
Requires:       python2-jsonpickle
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname} %{desc}

%if %{with python3}
%package -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-jsonpickle
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

%if %{with tests}
%check
python setup.py test
%if %{with python3}
python3 setup.py test
%endif
%endif

%files -n        python2-%{pkgname}
%doc README.md AUTHORS
%license LICENSE
%if 0%{?rhel} == 7
%{python_sitelib}/*
%else
%{python2_sitelib}/*
%endif

%if %{with python3}
%files -n         python3-%{pkgname}
%doc README.md AUTHORS
%license LICENSE
%{python3_sitelib}/*
%endif

%changelog
* Wed Aug  1 2018 Satoru SATOH <ssato@redhat.com> - 3.3.0-1
- Initial packaging
