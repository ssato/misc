# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%if 0%{?fedora}
%global with_python3 1
%endif

%define debug_package %{nil}
%define pymodname patsy

Name:           python-%{pymodname}
Version:        0.2.1
Release:        1%{?dist}
Summary:        A python library to describe statistical models and build design matrices
License:        BSD
Group:          Development/Languages
URL:            http://patsy.readthedocs.org
Source0:        https://pypi.python.org/packages/source/p/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       numpy
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
A Python library for describing statistical models (especially linear models,
or models that have a linear component) and building design matrices. Patsy
brings the convenience of R "formulas" to Python.

%if 0%{?with_python3}
%package -n     python3-%{pymodname}
Summary:        A python library to describe statistical models and build design matrices
Requires:       python3-numpy

%description -n python3-%{pymodname}
A Python library for describing statistical models (especially linear models,
or models that have a linear component) and building design matrices. Patsy
brings the convenience of R "formulas" to Python.

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
%doc README TODO
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n       python3-%{pymodname}
%defattr(644,root,root,755)
%doc README TODO
%{python3_sitelib}/*
%endif

%changelog
* Sun Jan 12 2014 Satoru SATOH <ssato@redhat.com> - 0.2.1-1
- Initial packaging
- 
