# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%define mname   Pillow

Name:           python-%{mname}
Version:        1.7.8
Release:        1%{?dist}
Summary:        Python Imaging Library forked from PIL
License:        Python
URL:            http://github.com/python-imaging/Pillow/
Source0:        https://pypi.python.org/packages/source/P/%{mname}/%{mname}-%{version}.zip
#BuildArch:      noarch
BuildRequires:  python-devel, python-setuptools
BuildRequires:  libjpeg-devel, zlib-devel, freetype-devel, lcms-devel
Requires:       python
Requires:       libjpeg, zlib, freetype, lcms


%description
Pillow is the "friendly" PIL fork. PIL is the Python Imaging Library. Pillow
was started for and is currently maintained by the Plone community. But it is
used by many other folks in the Python web community, and probably elsewhere
too.


%package        tools
Summary:        Tools distributed in %{mname}
Requires:       %{name} = %{version}-%{release}


%description    tools
Some tools distributed along with %{mname}.


%prep
%setup -q -n %{mname}-%{version}


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%files
%doc README.rst
# For noarch packages: sitelib
#%{python_sitelib}/*
# For arch-specific packages: sitearch
%{python_sitearch}/*


%files          tools
%doc README.rst
%{_bindir}/*


%changelog
* Tue Mar 12 2013 Satoru SATOH <ssato@redhat.com> - 1.7.8-1
- Initial packaging.
