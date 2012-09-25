# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define _url    http://trac-hacks.org/wiki/MultiRepoSearchPlugin
%define _url_avail  %(curl --silent %{_url} > /dev/null  && echo 1 || echo 0)


Name:           trac-multireposearch-plugin
Version:        0.3dev
Release:        1%{?dist}
Summary:        Source code repository search plugin for Trac
Group:          Applications/Internet
License:        BSD
URL:            %{_url}
#
# Source comes from git:
#  git clone git://github.com/boldprogressives/trac-MultiRepoSearchPlugin.git ...
#
Source0:        trac-MultiRepoSearchPlugin-%{version}.tar.bz2
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
This plugin allows users to search the source code repository.


%prep
%setup -n "trac-MultiRepoSearchPlugin-%{version}" -q


%build
%{__python} setup.py build
%if %{_url_avail}
w3m -dump %{_url} | sed -n '/^Description/,/^Contributors/p' > README.Fedora
%endif


%install
rm -rf $RPM_BUILD_ROOT
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
* Tue Sep 25 2012 Satoru SATOH <ssato@redhat.com> - 0.3dev-1
- Initial build
