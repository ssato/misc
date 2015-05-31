# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%if 0%{?fedora}
# NOTE: The code in **/examples/ contains print statement so that incompatible
# w/ py3k. It's not hard to fix them all but takes some time.
#%global with_python3 1
%global with_python3 0
%endif

%define debug_package %{nil}
%define pymodname statsmodels

Name:           python-%{pymodname}
Version:        0.5.0
Release:        1%{?dist}
Summary:        Statistical computations and models for use with SciPy
License:        BSD
Group:          Development/Languages
URL:            http://statsmodels.sourceforge.net
Source0:        https://pypi.python.org/packages/source/s/%{pymodname}/%{pymodname}-%{version}.tar.gz
Patch0:         statsmodels-0.5.0_disable_runtime_dep_check.patch
#BuildArch:      noarch
BuildRequires:  Cython
BuildRequires:  numpy
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
Requires:       numpy
Requires:       scipy
Requires:       python-pandas
Requires:       python-patsy
#Requires:       python-matplotlib
%if 0%{?with_python3}
BuildRequires:  python3-Cython
BuildRequires:  python3-devel
BuildRequires:  python3-numpy
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx
Requires:       python3-numpy
Requires:       python3-scipy
Requires:       python3-pandas
Requires:       python3-patsy
#Requires:       python3-matplotlib
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
%patch0 -p1 -b.disable_runtime_dep_check

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
# NOTE: These are not work w/ py3k because of 'print' statement. It's not too
# difficult to fix them all but takes some time so that just moves right now.
mv statsmodels/examples ./examples_py2
%endif

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
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
%doc README.txt README_l1.txt examples docs
# TODO: Build and make generated doc files included.
#%doc docs
# TODO: It seems upstream bug that noarch .py installed into arch-dependend dirs.
#%{python_sitelib}/*
%{python_sitearch}/*

%if 0%{?with_python3}
%files -n       python3-%{pymodname}
%defattr(644,root,root,755)
%doc README.txt README_l1.txt examples
%doc examples_py2
#%{python3_sitelib}/*
%{python3_sitearch}/*
%endif

%changelog
* Sun Jan 12 2014 Satoru SATOH <ssato@redhat.com> - 0.5.0-1
- Initial packaging
- 
