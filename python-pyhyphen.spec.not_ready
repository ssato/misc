# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%define pname   pyhyphen


Name:           python-%{pname}
Version:        1.0beta1
Release:        1%{?dist}
Summary:        A Python implementation of the hyphenation algorithm used in TeX and OpenOffice
License:        GPLv2+
URL:            http://code.google.com/p/pyhyphen/
Source0:        PyHyphen-%{version}.tar.gz
BuildRequires:  python-devel


%description
PyHyphen is a Python implementation of the hyphenation algorithm used in TeX
and OpenOffice based on 'libhyphen' C library originally from hnjlib.


%prep
%setup -q -n PyHyphen-%{version}


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%files
%doc README.txt ToDo.txt LICENSE.txt
%doc Doc
%{python_sitelib}/*
%{python_sitearch}/*


%changelog
* Fri Feb 17 2012 Satoru SATOH <ssato@redhat.com> - 1.0beta1-1
- Initial build.
