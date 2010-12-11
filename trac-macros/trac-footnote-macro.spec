# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define _url    http://trac-hacks.org/wiki/FootNoteMacro


Name:           trac-footnote-macro
Version:        1.03
Release:        1%{?dist}
Summary:        Wiki footnote macro for Trac
Group:          Applications/Internet
License:        BSD
URL:            %{_url}
#
# Source comes from SVN:
#  svn co http://trac-hacks.org/svn/footnotemacro/0.11/ t && \
#  cd t && python setup.py sdist --formats bztar
#
Source0:        FootNoteMacro-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  w3m
Requires:       trac >= 0.11, python-setuptools


%description
The FootNoteMacro automatically collates1 and generates footnotes.


%prep
%setup -n FootNoteMacro-%{version} -q


%build
%{__python} setup.py build
w3m -dump %{_url} > README.Fedora


%install
rm -rf $RPM_BUILD_ROOT
# skip-build doesn't work on el4
%{__python} setup.py install -O1 --root $RPM_BUILD_ROOT


 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.Fedora
%{python_sitelib}/*


%changelog
* Sun Dec 12 2010 Satoru SATOH <satoru.satoh+github@gmail.com> - 1.03-1
- Initial build
