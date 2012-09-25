# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%if 0%{?fedora} <= 12 && 0%{?rhel} <= 5
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif
%define _url    http://trac-hacks.org/wiki/IncludeMacro

#%define svnrev  @SVNREV@
%define svnrev  0

Name:           trac-include-macro
Version:        3.0.0dev
Release:        1svn%{svnrev}%{?dist}
Summary:        Wiki include macro for Trac
Group:          Applications/Internet
License:        BSD
URL:            %{_url}
#
# Source comes from SVN:
#  svn co http://trac-hacks.org/svn/includemacro/trunk/ t && \
#  cd t && python setup.py sdist --formats bztar
#
Source0:        TracIncludeMacro-%{version}-r%{svnrev}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       trac >= 0.12, python-setuptools


%description
This trac macro lets you include various things. Currently supported sources
are http, https, ftp, wiki pages and repository files. The default source is
wiki if only a source path is given.


%prep
%setup -n TracIncludeMacro-%{version}-r%{svnrev} -q


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
* Tue Sep 25 2012 Satoru SATOH <ssato@redhat.com> - 3.0.0dev-1svn0
- New upstream

* Thu Jul 12 2011 Satoru SATOH <satoru.satoh+github@gmail.com> - 2.1-r10462.1
- Clean up spec
- Embedded svn revision in release tag

* Sun Dec 12 2010 Satoru SATOH <satoru.satoh+github@gmail.com> - 2.1-1
- Initial build
