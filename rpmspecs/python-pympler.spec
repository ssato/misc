# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%define debug_package %{nil}

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-pympler
Version:        0.3.1
Release:        1%{?dist}
Summary:        A python library to measure, monitor and analyze the memory behavior of Python objects
License:        ASL 2.0
Group:          Development/Languages
URL:            http://pythonhosted.org/Pympler/
Source0:        https://pypi.python.org/packages/source/P/Pympler/Pympler-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
Pympler is a development tool to measure, monitor and analyze the memory
behavior of Python objects in a running Python application.

By pympling a Python application, detailed insight in the size and the lifetime
of Python objects can be obtained. Undesirable or unexpected runtime behavior
like memory bloat and other "pymples" can easily be identified.

Pympler integrates three previously separate projects into a single,
comprehensive profiling tool. Asizeof provides basic size information for one
or several Python objects, muppy is used for on-line monitoring of a Python
application and the class tracker provides off-line analysis of the lifetime of
selected Python objects. A web profiling frontend exposes process statistics,
garbage visualisation and class tracker statistics.

%if 0%{?with_python3}
%package -n     python3-pympler
Summary:        A python library to measure, monitor and analyze the memory behavior of Python objects

%description -n python3-pympler
Pympler is a development tool to measure, monitor and analyze the memory
behavior of Python objects in a running Python application.

This is a package for python-3.
%endif

%prep
%setup -q -n Pympler-%{version}

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
%doc NOTICE README.md doc
%{python_sitelib}/*
%{_datadir}/pympler/templates

%if 0%{?with_python3}
%files -n       python3-pympler
%defattr(644,root,root,755)
%doc NOTICE README.md doc
%{python3_sitelib}/*
%endif

%changelog
* Tue Jan 27 2015 Satoru SATOH <ssato@redhat.com> - 0.3.1-1
- Initial packaging
- 
