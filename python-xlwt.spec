# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}


Name:           python-xlwt
Version:        0.7.2
Release:        3%{?dist}
Summary:        A library to create Microsoft Excel (tm) spreadsheet files
Group:          Development/Languages
License:        BSD
URL:            http://pypi.python.org/pypi/xlwt
Source0:        http://pypi.python.org/packages/source/x/xlwt/xlwt-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel


%description
Xlwt is a library for generating spreadsheet files that are compatible with
Excel 97/2000/XP/2003, OpenOffice.org Calc, and Gnumeric. xlwt has full support
for Unicode. Excel spreadsheets can be generated on any platform without
needing Excel or a COM server. The only requirement is Python 2.3 to 2.6.
xlwt is a fork of pyExcelerator.

It may be recommended to to install python-xlrd along with this package for
reading Excel spreadsheets.


%prep
%setup -q -n xlwt-%{version}


%build
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{python_sitelib}/*


%changelog
* Wed Feb  1 2012 Satoru SATOH <ssato@redhat.com> - 0.7.2-3
- Embedded url in source0
- Removed some missing file entries

* Wed Jan  5 2011 Satoru SATOH <ssato@redhat.com> - 0.7.2-2
- deltarpm test

* Mon Aug 10 2009 Satoru SATOH <ssato@redhat.com> - 0.7.2-1
- Initial packaging.
