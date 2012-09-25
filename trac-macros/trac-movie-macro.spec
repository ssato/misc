# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%if 0%{?fedora} <= 12 && 0%{?rhel} <= 5
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif
%define _url    http://trac-hacks.org/wiki/MovieMacro
%define _url_avail  %(curl --silent %{_url} > /dev/null  && echo 1 || echo 0)

%define svnrev  0

Name:           trac-movie-macro
Version:        0.2dev
Release:        1svn%{svnrev}%{?dist}
Summary:        Wiki movie macro for Trac
Group:          Applications/Internet
License:        BSD
URL:            %{_url}
#
# Source comes from SVN:
#  svn co http://trac-hacks.org/svn/moviemacro/0.11/ t && \
#  cd t && python setup.py sdist --formats bztar
#
Source0:        MovieMacro-%{version}-r%{svnrev}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  curl
%if %{_url_avail}
BuildRequires:  w3m
%endif
Requires:       trac >= 0.12, python-setuptools


%description
Embed online movies from YouTube, GoogleVideo and MetaCafe, and local movies
via FlowPlayer. If you want support for more online sites just create a ticket.


%prep
%setup -n MovieMacro-%{version}-r%{svnrev} -q


%build
%{__python} setup.py build
%if %{_url_avail}
w3m -dump %{_url} | sed -n '/^Description/,/^Recent/p' > README.Fedora
%endif


%install
rm -rf $RPM_BUILD_ROOT
# skip-build doesn't work on el4
%{__python} setup.py install -O1 --root $RPM_BUILD_ROOT

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%if %{_url_avail}
%doc README.Fedora
%endif
%{python_sitelib}/*


%changelog
* Tue Sep 25 2012 Satoru SATOH <ssato@redhat.com> - 0.2-1
- New upstream

* Thu Jul 14 2011 Satoru SATOH <satoru.satoh+github@gmail.com> - 0.1-2
- Minor spec fixes

* Sun Dec 12 2010 Satoru SATOH <satoru.satoh+github@gmail.com> - 0.1-1
- Initial build
