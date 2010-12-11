# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define _url    http://trac-hacks.org/wiki/IncludeMacro


Name:           trac-include-macro
Version:        2.1
Release:        1%{?dist}
Summary:        Wiki include macro for Trac
Group:          Applications/Internet
License:        BSD
URL:            %{_url}
#
# Source comes from SVN:
#  svn co http://trac-hacks.org/svn/includemacro/0.11/ t && \
#  cd t && python setup.py sdist --formats bztar
#
Source0:        TracIncludeMacro-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       trac >= 0.11, python-setuptools


%description
This trac macro lets you include various things. Currently supported sources
are http, https, ftp, wiki pages and repository files. The default source is
wiki if only a source path is given.


%prep
%setup -n TracIncludeMacro-%{version} -q


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
# skip-build doesn't work on el4
%{__python} setup.py install -O1 --root $RPM_BUILD_ROOT


 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README
%{python_sitelib}/*


%changelog
* Sun Dec 12 2010 Satoru SATOH <satoru.satoh+github@gmail.com> - 2.1-1
- Initial build
