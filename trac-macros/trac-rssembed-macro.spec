# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define _url    http://trac-hacks.org/wiki/RssEmbedMacro


Name:           trac-rssembed-macro
Version:        0.0.1
Release:        1%{?dist}
Summary:        Wiki rssembed macro for Trac
Group:          Applications/Internet
License:        BSD
URL:            %{_url}
#
# Source comes from SVN:
#  svn co http://trac-hacks.org/svn/rssembedmacro/0.11/ t && \
#  cd t && python setup.py sdist --formats bztar
#
Source0:        TracRssEmbedMacro-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       trac >= 0.11, python-setuptools


%description
The trac macro to embed a RSS feed into a wiki page. All HTML is stripped out.


%prep
%setup -n TracRssEmbedMacro-%{version} -q


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
* Sun Dec 12 2010 Satoru SATOH <satoru.satoh+github@gmail.com> - 0.0.1-1
- Initial build
