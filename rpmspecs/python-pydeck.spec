%global pkgname pydeck
%global desc \
The pydeck library is a set of Python bindings for making spatial \
visualizations with deck.gl, optimized for a Jupyter Notebook \
environment.

%bcond_with tests

Name:           python-%{pkgname}
Version:        0.3.1
Release:        1%{?dist}
Summary:        Large-scale interactive data visualization in Python
License:        ASL 2.0
URL:            https://github.com/visgl/deck.gl/tree/master/bindings/pydeck
Source0: %{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-jinja2
%if %{with tests}
BuildRequires:  python3-nose
BuildRequires:  python3-flake8
BuildRequires:  python3-coverage
%endif

%description    %{desc}

%package -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-ipykernel
Requires:       python3-ipython
Requires:       python3-traitlets
Requires:       python3-jinja2
Requires:       python3-numpy
# Available from https://copr.fedorainfracloud.org/coprs/ssato/streamlit/ 
Requires:       python3-ipywidgets
#Requires:       python3-wheel
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desc}

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py3_build

%install
%py3_install

# dirty hack
mv %{buildroot}/{usr/etc,}

%if %{with tests}
%check
tox -e py$(python -c "import sys; sys.stdout.write(sys.version[:3].replace('.', ''))")
%endif

%files -n python3-%{pkgname}
%doc *.md docs examples
%license LICENSE.txt
%{python3_sitelib}/*
%{_sysconfdir}/jupyter/nbconfig/notebook.d/pydeck.json
%{_datadir}/jupyter/nbextensions/pydeck/*.*

%changelog
* Tue Jun 16 2020 Satoru SATOH <satoru.satoh@gmail.com> - 0.3.1-1
- Initial packaging
