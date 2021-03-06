# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}


Name:           python-xlutils
Version:        1.6.0
Release:        1%{?dist}
Summary:        Utilities for working with Excel files
Group:          Development/Languages
License:        MIT
URL:            http://pypi.python.org/pypi/xlutils
Source0:        http://pypi.python.org/packages/source/x/xlutils/xlutils-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-xlrd
Requires:       python-xlwt
# for testing:
#Requires:       python-errorhandler
#Requires:       python-manuel
#Requires:       python-mock
#Requires:       python-testfixtures >= 1.6.1


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


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

# The followings are packaged as doc.
rm -rf $RPM_BUILD_ROOT%{python_sitelib}/xlwt/{doc,examples}

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.txt docs
%{python_sitelib}/*
%{_bindir}/margins


%changelog
* Fri Jul 26 2013 Satoru SATOH <ssato@redhat.com> - 1.6.0-1
- New upstream release
- Removed README.Fedora.txt as upstream version now contains README.txt
- Fixed runtime dependencies

* Mon Mar 26 2012 Satoru SATOH <ssato@redhat.com> - 1.5.1-1
- New upstream release

* Wed Feb  1 2012 Satoru SATOH <ssato@redhat.com> - 1.4.1-2
- Embedded url in source0

* Wed Feb  1 2012 Satoru SATOH <ssato@redhat.com> - 1.4.1-1
- New upstream release

* Mon Aug 10 2009 Satoru SATOH <ssato@redhat.com> - 1.3.2-1
- Initial packaging.
