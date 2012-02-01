# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}


Name:           python-xlutils
Version:        1.4.1
Release:        1%{?dist}
Summary:        Utilities for working with Excel files
Group:          Development/Languages
License:        MIT
URL:            http://pypi.python.org/pypi/xlutils
Source0:        xlutils-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-xlrd
Requires:       python-xlwt
Requires:       python-errorhandler


%description
Utilities for working with Excel files that require both xlrd and xlwt written
in Python.

This package provides a collection of utilities for working with Excel files.
Since these utilities may require either or both of the xlrd and xlwt packages,
they are collected together seperately here.


%prep
%setup -q -n xlutils-%{version}


%build
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

cat << EOF > README.Fedora.rst
This package provides a collection of utilities for working with Excel files.
Since these utilities may require either or both of the xlrd and xlwt packages,
they are collected together seperately here.

Currently available are:

xlutils.copy
    Tools for copying xlrd.Book objects to xlwt.Workbook objects.
xlutils.display
    Utility functions for displaying information about xlrd-related objects in a user-friendly and safe fashion.
xlutils.filter
    A mini framework for splitting and filtering Excel files into new Excel files.
xlutils.margins
    Tools for finding how much of an Excel file contains useful data.
xlutils.save
    Tools for serializing xlrd.Book objects back to Excel files.
xlutils.styles
    Tools for working with formatting information expressed in styles. 
EOF


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.Fedora.rst
%{python_sitelib}/*
%{_bindir}/margins


%changelog
* Wed Feb  1 2012 Satoru SATOH <ssato@redhat.com> - 1.4.1-1
- New upstream release

* Mon Aug 10 2009 Satoru SATOH <ssato@redhat.com> - 1.3.2-1
- Initial packaging.
