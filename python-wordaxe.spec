# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define  modname  wordaxe


Name:           python-%{modname}
Version:        1.0.1
Release:        2%{?dist}
Summary:        Hyphenation by decomposition of compound words
Group:          Development/Languages
License:        ASL 2.0
URL:            http://pypi.python.org/pypi/errorhandler
Source0:        %{modname}-%{version}.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
Requires:       python-pyhyphen


%description
A library (formerly known as deco-cow) provides Python programs with the
ability to automatically hyphenate words using some algorithms.


%prep
%setup -q -n %{modname}-%{version}


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc docs/* 
%doc htdocs
%{python_sitelib}/*


%changelog
* Fri Feb 17 2012 Satoru SATOH <ssato@redhat.com> - 1.0.1-2
- Some cleanups
- Added runtime dependency to python-pyhyphen

* Tue Jun 28 2011 Satoru SATOH <ssato@redhat.com> - 1.0.1-1
- Initial packaging.
