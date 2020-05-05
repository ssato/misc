# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global arcname plotly.py
%global pkgname plotly
%global desctxt \
The plotly Python library (plotly.py) is an interactive, open-source plotting \
library that supports over 40 unique chart types covering a wide range of \
statistical, financial, geographic, scientific, and 3-dimensional use-cases.

%define py_setup packages/python/plotly/setup.py

Name:           python-%{pkgname}
Version:        4.6.0
Release:        1%{?dist}
Summary:        Python graphing library makes interactive, publication-quality graphs
Group:          Development/Libraries
License:        MIT
URL:            https://plot.ly/python/
Source0:        %{arcname}-%{version}.tar.gz
#Patch0:         plotly-4.3.0-jupyter-sysconfdir.patch
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description %{desctxt}

%package     -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-retrying >= 1.3.3
Requires:       python3-six
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desctxt}

%prep
%autosetup -n %{arcname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{pkgname}
%doc README.md
%{python3_sitelib}/*
%{_sysconfdir}/jupyter/nbconfig/notebook.d/*.json
%{_datadir}/jupyter/nbextensions/plotlywidget/*.js

%changelog
* Wed May  6 2020 Satoru SATOH <satoru.satoh@gmail.com> - 4.6.0-1
- New upstream

* Sat Nov 16 2019 Satoru SATOH <satoru.satoh@gmail.com> - 4.3.0-1
- Initial packaging
