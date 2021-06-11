# SEEALSO:
# - https://fedoraproject.org/wiki/Packaging:Python
# - https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/
#
%global srcname pytest-profiling
%global desctxt \
Profiling plugin for pytest, with tabular and heat graph output.\
\
Tests are profiled with cProfile and analysed with pstats; heat graphs are\
generated using gprof2dot and dot.

Name:           python-%{srcname}
Version:        1.7.0
Release:        1%{?dist}
Summary:        Profiling plugin for pytest
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/man-group/pytest-plugins/tree/master/pytest-profiling
Source0:        %pypi_source
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_git
BuildRequires:  python3-pip
BuildRequires:  python3-pytest-virtualenv
BuildRequires:  python3-wheel

%description    %{desctxt}

%package     -n python3-%{srcname}
Summary:        %{summary}
Requires:       python3-six
Requires:       python3-pytest
Requires:       gprof2dot
%py_provides python3-%{srcname}
# avoid 'nothing provides python3.9dist(gprof2dot)' error
%{?python_disable_dependency_generator}

%description -n python3-%{srcname} %{desctxt}

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{srcname}
%doc README.md docs/static
%{python3_sitelib}/*

%changelog
* Fri Jun 11 2021 Satoru SATOH <satoru.satoh@gmail.com> - 1.7.0-1
- Initial packaging
