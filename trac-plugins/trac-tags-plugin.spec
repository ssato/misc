# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define _url    http://trac-hacks.org/wiki/TagsPlugin
%define _url_avail  %(curl --silent %{_url} > /dev/null  && echo 1 || echo 0)


Name:           trac-tags-plugin
Version:        0.6
Release:        1%{?dist}
Summary:        Tags plugin for Trac
Group:          Applications/Internet
License:        BSD
URL:            %{_url}
#
# Source comes from SVN:
#  svn co http://trac-hacks.org/svn//tagsplugin/tags/0.6/ && \
#  cd 0.6 && python setup.py sdist --formats bztar
#
Source0:        TracTags-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  curl
%if %{_url_avail}
BuildRequires:  w3m
%endif
Requires:       trac >= 0.11, python-setuptools, python-genshi >= 0.5


%description
The TagsPlugin implements both a generic tagging engine, and frontends for the
Wiki and ticket systems. An extra text entry box is added to the Wiki edit page
for tagging Wiki pages, and ticket fields (you can configure which ones) are
treated as tags for the ticket system.


%prep
%setup -n TracTags-%{version} -q


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
* Sun Dec 05 2010 Satoru SATOH <satoru.satoh+github@gmail.com> - 0.6-1
- Initial build
