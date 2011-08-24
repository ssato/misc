# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}


Name:           python-wordaxe
Version:        1.0.1
Release:        1%{?dist}
Summary:        Hyphenation by decomposition of compound words
Group:          Development/Languages
License:        ASL 2.0
URL:            http://pypi.python.org/pypi/errorhandler
Source0:        wordaxe-%{version}.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel


%description
A library (formerly known as deco-cow) provides Python programs with the
ability to automatically hyphenate words using an algorithm which is based on
decomposition of compound words into base words, and is named DCWHyphenator in
the code.


%prep
%setup -q -n wordaxe-%{version}


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
%doc docs/* 
%doc htdocs
%{python_sitelib}/*


%changelog
* Tue Jun 28 2011 Satoru SATOH <ssato@redhat.com> - 1.0.1-1
- Initial packaging.
