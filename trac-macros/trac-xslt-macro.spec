# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define _url    http://trac-hacks.org/wiki/XsltMacro
%define _url_avail  %(curl --silent %{_url} > /dev/null  && echo 1 || echo 0)


Name:           trac-xlst-macro
Version:        0.8
Release:        1%{?dist}
Summary:        Wiki xlst macro for Trac
Group:          Applications/Internet
License:        BSD
URL:            %{_url}
#
# Source comes from SVN:
#  svn co http://trac-hacks.org/svn/xlstmacro/0.11/ t && \
#  cd t && python setup.py sdist --formats bztar
#
Source0:        xslt-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  w3m
BuildRequires:  curl
Requires:       trac >= 0.11, python-setuptools
Requires:       libxml2-python, libxslt-python


%description
The XsltMacro allows you to embed the result of an XSL-transformation in a
page. It takes two parameters, a stylesheet and a document to transform. These
can be an attachment on any wiki-page or ticket, any page from the htdocs area,
any file in the repository, or any url (these options are similar to those for
Trac's native ImageMacro). For more details see the documentation in the macro.

The macro can either be installed as a simple macro or as a plugin; the
use_iframe and use_object options (see below) only work when installed as a
plugin.


%prep
%setup -n xslt-%{version} -q


%build
%{__python} setup.py build
%if %{_url_avail}
w3m -dump %{_url} | sed -n '/^Description/,/^Attachments/p' > README.Fedora
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
* Sun Dec 12 2010 Satoru SATOH <satoru.satoh+github@gmail.com> - 0.8-1
- Initial build
