# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%if 0%{?fedora}
%global with_python3 1
%endif

%define debug_package %{nil}
%define pymodname seaborn

Name:           python-%{pymodname}
Version:        0.2.0
Release:        1%{?dist}
Summary:        Python library for statistical data visualization
License:        BSD
Group:          Development/Languages
URL:            https://github.com/mwaskom/seaborn
#Source0:        https://github.com/mwaskom/%{pymodname}/archive/v%{version}.tar.gz
Source0:        %{pymodname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       numpy
Requires:       scipy
Requires:       python-matplotlib
Requires:       python-pandas
Requires:       python-statsmodels
Requires:       pyhusl
Requires:       python-moss
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
Seaborn is a library of high-level functions that facilitate making informative
and attractive plots of statistical data using matplotlib. It also provides
concise control over the aesthetics of the plots, improving on matplotlib's
default look.

%if 0%{?with_python3}
%package -n     python3-%{pymodname}
Summary:        Python library for neroimaging and cognitive data analysis
Requires:       python3-numpy
Requires:       python3-scipy
Requires:       python3-matplotlib
Requires:       python3-pandas
Requires:       python3-statsmodels
Requires:       python3-pyhusl
Requires:       python3-moss

%description -n python3-%{pymodname}
Seaborn is a library of high-level functions that facilitate making informative
and attractive plots of statistical data using matplotlib. It also provides
concise control over the aesthetics of the plots, improving on matplotlib's
default look.

This is a package for python-3.
%endif

%prep
%setup -q -n %{pymodname}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif
 
%files
%doc README.md doc examples
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n       python3-%{pymodname}
%defattr(644,root,root,755)
%doc README.md doc examples
%{python3_sitelib}/*
%endif

%changelog
* Mon Jan 13 2014 Satoru SATOH <ssato@redhat.com> - 0.2.0-1
- Initial packaging
