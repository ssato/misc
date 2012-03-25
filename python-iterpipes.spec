# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define modname iterpipes


Name:           python-iterpipes
Version:        0.4
Release:        1%{?dist}
Summary:        A python library for running shell pipelines using shell-like syntax
Group:          Development/Languages
License:        MIT
URL:            http://pypi.python.org/pypi/%{modname}
Source0:        http://pypi.python.org/packages/source/i/%{modname}/%{modname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel


%description
Pipelines is a python library for running shell pipelines using shell-like syntax.

 * Enables piping infinite streams through shell pipelines in Python
 * Represents a shell command as an ordinary function Iterable -> Iterable
 * Allows mixing shell commands and Python functions in a single pipeline
 * Uses standard interprocessing modules subprocess, threading
 * Allows doing things marked as red warning boxes at the subprocess help page
 * 0.2 KLOC, tests included



%prep
%setup -q -n iterpipes-%{version}


%build
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README TODO
%{python_sitelib}/*


%changelog
* Mon Mar 26 2012 Satoru SATOH <ssato@redhat.com> - 0.4-1
- New upstream release

* Sun Dec 27 2009 Satoru SATOH <ssato@redhat.com> - 0.3-1
- Initial packaging.
