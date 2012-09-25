# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define _url    http://trac-hacks.org/wiki/DefaultCcPlugin
%define _url_avail  %(curl --silent %{_url} > /dev/null  && echo 1 || echo 0)
%define svnrev 0
%define svnver 0.3dev-r0


Name:           trac-defaultcc-plugin
Version:        0.3dev
Release:        1svn%{svnrev}%{?dist}
Summary:        Default Cc plugin for Trac
Group:          Applications/Internet
License:        BSD
URL:            %{_url}
#
# Source comes from SVN:
#  svn co http://trac-hacks.org/svn/defaultccplugin/trunk/ && \
#  cd trunk && python setup.py sdist --formats bztar
#
Source0:        DefaultCc-%{version}-r%{svnrev}.tar.bz2
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
Automatically adds a default CC list when a new ticket is created, based on its
initial component. Tickets are modified right after their creation to add the
component's default CC list to the ticket CC list. CC lists can be configured
per component through the component's admin UI.


%prep
%setup -n "DefaultCc-%{version}-r%{svnrev}" -q


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
* Tue Sep 25 2012 Satoru SATOH <ssato@redhat.com> - 0.3dev-1svn0
- Rebase to new upstream

* Sun Dec 05 2010 Satoru SATOH <satoru.satoh+github@gmail.com> - 0.1-1svn5293
- Initial build
