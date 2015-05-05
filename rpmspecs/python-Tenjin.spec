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
%define pymodname Tenjin

Name:           python-%{pymodname}
Version:        1.1.1
Release:        1%{?dist}
Summary:        A fast and full-featured template engine based on embedded Python
License:        MIT
Group:          Development/Languages
URL:            http://www.kuwata-lab.com/tenjin/
Source0:        https://pypi.python.org/packages/source/T/%{pymodname}/%{pymodname}-%{version}.tar.gz
#Source0:        %{pymodname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python
Requires:       python
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3
%endif

%description
pyTenjin is a very fast and full-featured template engine. You can embed Python
statements and expressions into your template file. pyTenjin converts it into
Python script and evaluate it.

%if 0%{?with_python3}
%package -n     python3-%{pymodname}
Summary:        A python interactive visualization library for large datasets that natively uses the latest web technologies
Requires:       python3

%description -n python3-%{pymodname}
pyTenjin is a very fast and full-featured template engine. You can embed Python
statements and expressions into your template file. pyTenjin converts it into
Python script and evaluate it.

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
sed 's,/usr/bin/env python,/usr/bin/python3,' $RPM_BUILD_ROOT%{_bindir}/pytenjin \
        > $RPM_BUILD_ROOT%{_bindir}/py3tenjin
popd
%endif
 
%files
%doc CHANGES.txt README.txt benchmark doc examples
%{python_sitelib}/*
%{_bindir}/pytenjin

%if 0%{?with_python3}
%files -n       python3-%{pymodname}
%defattr(644,root,root,755)
%doc CHANGES.txt README.txt benchmark doc examples
%{python3_sitelib}/*
%{_bindir}/py3tenjin
%endif

%changelog
* Tue May  5 2015 Satoru SATOH <ssato@redhat.com> - 1.1.1-1
- Initial packaging
