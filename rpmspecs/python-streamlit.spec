%global pkgname streamlit
%global desc \
Streamlit lets you create apps for your machine learning projects with \
deceptively simple Python scripts. It supports hot-reloading, so your \
app updates live as you edit and save your file. No need to mess with \
HTTP requests, HTML, JavaScript, etc. All you need is your favorite \
editor and a browser.

%bcond_with tests

Name:           python-%{pkgname}
Version:        0.61.0
Release:        1%{?dist}
Summary:        Python library to build web-based custom ML tools fast
License:        ASL 2.0
URL:            https://github.com/streamlit/streamlit
Source0:        %{pkgname}-%{version}.tar.gz
# Patch0:         streamlit-0.61.0-makefile.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  pipenv
%if %{with tests}
BuildRequires:  python3-tox
BuildRequires:  python3-coveralls
BuildRequires:  python3-flake8
BuildRequires:  python3-nose
BuildRequires:  python3-pycodestyle
BuildRequires:  python3-pylint
%endif

%description    %{desc}

%package -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-blinker
Requires:       python3-boto3
Requires:       python3-botocore >= 1.13.44
Requires:       python3-cachetools
Requires:       python3-click
Requires:       python3-numpy
Requires:       python3-packaging
Requires:       python3-pandas
Requires:       python3-pillow
Requires:       python3-protobuf >= 3.11.2
Requires:       python3-dateutil
Requires:       python3-requests
Requires:       python3-toml
Requires:       python3-tornado
Requires:       python3-tzlocal
Requires:       python3-validators
Requires:       python3-watchdog
# Available from https://copr.fedorainfracloud.org/coprs/ssato/streamlit
Requires:       python3-altair
Requires:       python3-astor
Requires:       python3-base58
Requires:       python3-pydeck
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desc}

%prep
%autosetup -n %{pkgname}-%{version}

%build
# (cd lib; %%py3_build)

%install
(cd lib; %py3_install)

%if %{with tests}
%check
tox -e py$(python -c "import sys; sys.stdout.write(sys.version[:3].replace('.', ''))")
%endif

%files -n python3-%{pkgname}
%doc README.rst NEWS
%license LICENSE.MIT
%{python3_sitelib}/*
%{_bindir}/*

%changelog
* Sun May 17 2020 Satoru SATOH <satoru.satoh@gmail.com> - 0.3.0-1
- New upstream
- Add some runtime and test time dependencies

* Sat May  2 2020 Satoru SATOH <satoru.satoh@gmail.com> - 0.1.0-1
- Initial packaging
