# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}


Name:           trac-mscgen-plugin
Version:        0.1
Release:        1%{?dist}
Summary:        Mscgen plugin for Trac
Group:          Applications/Internet
License:        BSD
URL:            http://trac-hacks.org/wiki/MscgenPlugin
#
# Source comes from SVN:
#  svn co http://trac-hacks.org/svn/mscgenplugin/0.11/ t && \
#  cd t && python setup.py sdist --formats bztar
#
Source0:        mscgen-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       trac >= 0.11, python-setuptools
Requires:       mscgen


%description
MscgenPlugin provides a plugin for Trac to render mscgen message sequence chart
diagrams within a Trac wiki page.


%prep
%setup -n mscgen-%{version} -q


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --root $RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.txt
%{python_sitelib}/*


%changelog
* Sun Dec 05 2010 Satoru SATOH <satoru.satoh+github@gmail.com> - 0.1-1
- Initial build
