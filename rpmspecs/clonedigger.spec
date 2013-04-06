# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%global         unmangled_version 1.0.11-beta


Name:           clonedigger
Version:        1.0.11_beta
Release:        1%{?dist}
Summary:        Clone Digger aimed to detect similar code in Python and Java programs
License:        GPLv3+
Group:          Development/Libraries
URL:            http://clonedigger.sourceforge.net
Source0:        https://pypi.python.org/packages/source/c/clonedigger/%{name}-%{unmangled_version}.tar.gz       
BuildArch:      noarch
BuildRequires:  python-devel, python-setuptools


%description
Clone Digger is the tool for finding software clones, duplicated code fragments
in python source codes. 

Currently only Python language is supported, Java support will be added soon.
See the site for details.


%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%files
%doc clonedigger/README.txt
%{_bindir}/*
%{python_sitelib}/*


%changelog
* Sat Apr  6 2013 Satoru SATOH <ssato@redhat.com> - 1.0.11_beta-1
- Initial packaging.
