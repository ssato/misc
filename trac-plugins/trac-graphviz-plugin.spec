# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define svnrev 0


Name:           trac-graphviz-plugin
Version:        0.7.6
Release:        1svn%{svnrev}%{?dist}
Summary:        Graphviz plugin for Trac
Group:          Applications/Internet
License:        BSD
URL:            http://trac-hacks.org/wiki/GraphvizPlugin
#
# Source comes from SVN:
#  svn co http://trac-hacks.org/svn/graphvizplugin/0.11/ t && \
#  cd t && python setup.py sdist --formats bztar
#
Source0:        graphviz-%{version}dev-r%{svnrev}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       trac >= 0.11, python-setuptools
Requires:       graphviz


%description
The GraphvizPlugin allows for the inline creation of diagrams for abstract
graphs and networks using the Graphviz programs.


%prep
%setup -n graphviz-%{version}dev-r%{svnrev} -q


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --root $RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.txt ReleaseNotes.txt
%{python_sitelib}/*


%changelog
* Sun Dec 05 2010 Satoru SATOH <satoru.satoh+github@gmail.com> - 0.7.6-1
- Initial build
