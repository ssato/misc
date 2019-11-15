%global pypi_name sphinxcontrib-napoleon
%global common_desc \
Napoleon is a Sphinx extension that enables Sphinx to parse both NumPy and \
Google style docstrings - the style recommended by Khan Academy. \
\
Napoleon is a pre-processor that parses NumPy and Google style docstrings and \
converts them to reStructuredText before Sphinx attempts to parse them. This \
happens in an intermediate step while Sphinx is processing the documentation, \
so it doesn't modify any of the docstrings in your actual source code files. \

Name:           python-%{pypi_name}
Version:        0.7
Release:        1%{?dist}
Summary:        A Sphinx extension enables Sphinx to parse both NumPy and Google style docstrings
License:        BSD
URL:            https://sphinxcontrib-napoleon.readthedocs.io
Source0:        https://files.pythonhosted.org/packages/source/s/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-sphinx
BuildRequires:  python3-devel
BuildRequires:  python3-six
BuildRequires:  python3-sphinx
BuildRequires:  python3-setuptools

%description %common_desc

%package -n python3-%{pypi_name}
Summary:    %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
Requires:   python3-pbr
Requires:   python3-sphinx
Requires:   python3-pockets

%description -n python3-%{pypi_name} %common_desc

%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py3_build

%install
%py3_install

# %check
# py.test-3 ||

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/sphinxcontrib_napoleon*
%{python3_sitelib}/sphinxcontrib/napoleon
%{python3_sitelib}/sphinxcontrib_napoleon-%{version}-py?.?.egg-info

%changelog
* Fri Nov 15 2019 Satoru SATOH <satoru.satoh@gmail.com> - 0.7-1
- Initial package.
