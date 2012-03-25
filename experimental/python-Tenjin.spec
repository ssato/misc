%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}


Name:           python-Tenjin
Version:        1.0.1
Release:        1%{?dist}
Summary:        A fast and full-featured template engine based on embedded Python
Group:          Development/Languages
License:        MIT
URL:            http://pypi.python.org/pypi/Tenjin
Source0:        Tenjin-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel


%description
pyTenjin is a very fast and full-featured template engine. You can embed Python
statements and expressions into your template file. pyTenjin converts it into
Python script and evaluate it.

Features:

* Very fast
  * About x10 faster than Django, x4 than Cheetah, x2 than Mako
  * In addition loading tenjin.py is very lightweight (important for CGI)
* Full featured
  * Nestable layout template
  * Partial template
  * Fragment cache
  * Capturing
  * Preprocessing
* Easy to learn
  * You don't have to learn template-specific language
* Supports Google App Engine


%prep
%setup -q -n Tenjin-%{version}


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc CHANGES.txt README.txt
%doc doc
%doc examples
%{python_sitelib}/*
%{_bindir}/*


%changelog
* Tue Oct 11 2011 Satoru SATOH <ssato@redhat.com> - 1.0.1-1
- Initial packaging.
