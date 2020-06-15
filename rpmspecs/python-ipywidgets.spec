%global pkgname ipywidgets
%global desc \
Interactive HTML widgets for Jupyter notebooks and the IPython kernel.

%bcond_with tests

Name:           python-%{pkgname}
Version:        7.5.1
Release:        1%{?dist}
Summary:        Interactive HTML widgets for Jupyter notebooks and the IPython kernel
License:        ASL 2.0
URL:            http://ipython.org
Source0: %{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
%if %{with tests}
BuildRequires:  python3-nose
BuildRequires:  python3-flake8
BuildRequires:  python3-coverage
%endif

%description    %{desc}

%package -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-ipykernel
Requires:       python3-traitlets
Requires:       python3-nbformat
Requires:       python3-numpy
# NA but it does not look required. 
#Requires:       python3-widgetsnbextension
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
%doc *.md docs
%license LICENSE
%{python3_sitelib}/*

%changelog
* Tue Jun 16 2020 Satoru SATOH <satoru.satoh@gmail.com> - 7.5.1-1
- Initial packaging
