# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%if 0%{?fedora}
# NOTE: The upstream archive contains test and example code not runnable w/
# py3k. So disabled build for py3k for a while. (It seems that most of failures
# because of print statement not available in py3k so it's not pretty difficult
# to fix these but it takes some time, I guess.)
%global with_python3 1
%endif

%define debug_package %{nil}
%define pymodname pies

Name:           python-%{pymodname}
Version:        2.6.3
Release:        1%{?dist}
Summary:        python 2 and 3 compatibility layer module
License:        MIT
Group:          Development/Languages
URL:            https://github.com/timothycrosley/pies
Source0:        https://github.com/timothycrosley/%{pymodname}/archive/%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-pies
Requires:       python-natsort
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
Pies is a Python2 & 3 Compatibility layer with the philosophy that all code
should be Python3 code. Starting from this viewpoint means that when running on
Python3 pies adds virtually no overhead.

Instead of providing a bunch of custom methods (leading to Python code that
looks out of place on any version) pies aims to back port as many of the
Python3 api calls, imports, and objects to Python2 - Relying on special syntax
only when absolutely necessary.

%if 0%{?with_python3}
%package -n     python3-%{pymodname}
Summary:        An utility and library to sort Python imports
Requires:       python3-natsort

%description -n python3-%{pymodname}
isort is a Python utility / library to sort imports alphabetically, and
automatically separated into sections. It provides a command line utility,
Python library and plugins for various editors to quickly sort all your
imports. It currently cleanly supports Python 2.6 - 3.4 using pies
(https://github.com/timothycrosley/pies) to achieve this without ugly hacks
and/or py2to3.

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
%doc ACKNOWLEDGEMENTS.md README.md logo.png
%{python_sitelib}/*
%{_bindir}/isort

%if 0%{?with_python3}
%files -n       python3-%{pymodname}
%defattr(644,root,root,755)
%doc ACKNOWLEDGEMENTS.md README.md logo.png
%{python3_sitelib}/*
%endif

%changelog
* Sat Mar 14 2015 Satoru SATOH <ssato@redhat.com> - 3.9.6-1
- Initial packaging
