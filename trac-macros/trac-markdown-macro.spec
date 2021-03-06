Name:           trac-markdown-macro
Version:        0.11.1
Release:        3%{?dist}
Summary:        Wiki markdown macro for Trac
Group:          Applications/Internet
License:        BSD
URL:            http://trac-hacks.org/wiki/MarkdownMacro
#
# Source comes from github:
#  git clone git://github.com/dwclifton/tracmarkdownmacro.git t && \
#  cd t/0.11/ && python setup.py sdist --formats bztar
#
Source0:        TracMarkdownMacro-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       trac >= 0.12, python-setuptools, python-markdown


%description
The MarkdownMacro package implements John Gruber's Markdown lightweight plain
text-to-HTML formatting syntax as a WikiProcessor macro. The original code is
courtesy of Alex Mizrahi aka killer_storm. I simply added a little robustness
to the error checking, documented the package, created setup.py and this
README, and registered it with Trac Hacks.


%prep
%setup -n TracMarkdownMacro-%{version} -q


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --root $RPM_BUILD_ROOT

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README
%{python_sitelib}/*


%changelog
* Tue Sep 25 2012 Satoru SATOH <ssato@redhat.com> - 0.11.1-3
- Bumped up required version of trac from 11 to 12

* Thu Jul 14 2011 Satoru SATOH <satoru.satoh+github@gmail.com> - 0.11.1-2
- Minor spec fixes

* Sun Dec 12 2010 Satoru SATOH <satoru.satoh+github@gmail.com> - 0.11.1-1
- Initial build
