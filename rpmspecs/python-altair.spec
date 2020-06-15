%global pkgname altair
%global desc \
Altair is a declarative statistical visualization library for Python. \
With Altair, you can spend more time understanding your data and its \
meaning. Altair API is simple, friendly and consistent and built on \
top of the powerful Vega-Lite JSON specification. This elegant \
simplicity produces beautiful and effective visualizations with a \
minimal amount of code.

%bcond_with tests

Name:           python-%{pkgname}
Version:        4.1.0
Release:        1%{?dist}
Summary:        Declarative statistical visualization library for python
License:        BSD
URL:            https://altair-viz.github.io
Source0: %{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
%if %{with tests}
BuildRequires:  python3-flake8
BuildRequires:  python3-pytest
BuildRequires:  python3-jinja2
BuildRequires:  python3-sphinx
BuildRequires:  python3-m2r
BuildRequires:  python3-docutils
BuildRequires:  python3-ipython
# .. todo:: Make RPM.
BuildRequires:  python3-vega-datasets
%endif

%description    %{desc}

%package -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-entrypoints
Requires:       python3-jsonschema
Requires:       python3-numpy
Requires:       python3-pandas
Requires:       python3-toolz
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desc}

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py3_build

%install
%py3_install

%if %{with tests}
%check
tox -e py$(python -c "import sys; sys.stdout.write(sys.version[:3].replace('.', ''))")
%endif

%files -n python3-%{pkgname}
%doc *.md doc/ design/ doc/ images/ paper/
%license LICENSE
%{python3_sitelib}/*
#%%{_bindir}/*

%changelog
* Mon Jun 15 2020 Satoru SATOH <satoru.satoh@gmail.com> - 4.1.0-1
- Initial packaging
