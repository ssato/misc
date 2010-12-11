# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define _url    http://trac-hacks.org/wiki/MovieMacro
%define _url_avail  %(curl --silent %{_url} > /dev/null  && echo 1 || echo 0)


Name:           trac-movie-macro
Version:        0.1
Release:        1%{?dist}
Summary:        Wiki movie macro for Trac
Group:          Applications/Internet
License:        BSD
URL:            %{_url}
#
# Source comes from SVN:
#  svn co http://trac-hacks.org/svn/moviemacro/0.11/ t && \
#  cd t && python setup.py sdist --formats bztar
#
Source0:        MovieMacro-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  w3m
BuildRequires:  curl
Requires:       trac >= 0.11, python-setuptools


%description
Embed online movies from YouTube, GoogleVideo and MetaCafe, and local movies
via FlowPlayer. If you want support for more online sites just create a ticket.


%prep
%setup -n MovieMacro-%{version} -q


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
* Sun Dec 12 2010 Satoru SATOH <satoru.satoh+github@gmail.com> - 0.1-1
- Initial build
