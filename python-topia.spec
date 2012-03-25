# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}


Name:           python-topia
Version:        1.1.0
Release:        2%{?dist}
Summary:        Content Term Extraction library using POS Tagging
Group:          Development/Languages
License:        ZPL2.1
URL:            http://pypi.python.org/pypi/topia.termextract
Source0:        http://pypi.python.org/packages/source/t/topia.termextract/topia.termextract-%{version}.tar.gz
#Source1:        README.Fedora.rst
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools


%description
This package determines important terms within a given piece of content. It
uses linguistic tools such as Parts-Of-Speech (POS) and some simple statistical
analysis to determine the terms and their strength.


%prep
%setup -q -n topia.termextract-%{version}


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
# It looks missing:
mkdir -p $RPM_BUILD_ROOT%{python_sitelib}/topia
touch $RPM_BUILD_ROOT%{python_sitelib}/topia/__init__.py

%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.txt
%{python_sitelib}/*


%changelog
* Mon Mar 26 2012 Satoru SATOH <ssato@redhat.com> - 1.1.0-2
- Changed source0 to the complete url form for easy build

* Thu Sep 15 2011 Satoru SATOH <ssato@redhat.com> - 1.1.0-1
- Initial packaging.
