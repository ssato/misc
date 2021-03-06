# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%define _url    http://trac-hacks.org/wiki/FootNoteMacro
%define _url_avail  %(curl --silent %{_url} > /dev/null  && echo 1 || echo 0)

#%define svnrev  @SVNREV@
%define svnrev  0

Name:           trac-footnote-macro
Version:        1.03
Release:        1svn%{svnrev}%{?dist}
Summary:        Wiki footnote macro for Trac
Group:          Applications/Internet
License:        BSD
URL:            %{_url}
#
# Source comes from SVN:
#  svn co http://trac-hacks.org/svn/footnotemacro/trunk/ t && \
#  cd t && python setup.py sdist --formats bztar
#
Source0:        FootNoteMacro-%{version}-r%{svnrev}.tar.bz2
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
The FootNoteMacro automatically collates1 and generates footnotes.


%prep
%setup -n FootNoteMacro-%{version}-r%{svnrev} -q


%build
%{__python} setup.py build
%if %{_url_avail}
w3m -dump %{_url} | sed -n '/^Description/,/^Contributors/p' > README.Fedora
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
* Tue Sep 25 2012 Satoru SATOH <ssato@redhat.com> - 1.03-r11767.1
- New upstream

* Thu Jul 14 2011 Satoru SATOH <satoru.satoh+github@gmail.com> - 1.03-r10434.1
- python_sitelib looks defined in /etc/rpm/macros these days so that make it
  defined conditionaly

* Sun Dec 12 2010 Satoru SATOH <satoru.satoh+github@gmail.com> - 1.03-1
- Initial build
