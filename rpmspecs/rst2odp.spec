# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:           rst2odp
Version:        0.2.5
Release:        1%{?dist}
Summary:        Converter for rst to LibreOffice Impress
License:        Apache
URL:            https://github.com/mattharrison/rst2odp
Source0:        https://pypi.python.org/packages/source/r/rst2odp/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-docutils >= 0.10
Requires:       python-Pillow >= 1.7.8
# Optional for highlights:
#Requires:       python-pygments >= 1.6


%description
This package contains a Python script (rst2odp) to convert reStructuredText to
LibreOffice Impress (rst2odp). It also includes a general python library
(odplib/preso.py) for creating Impress files.


%prep
%setup -q


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%files
%doc README.rst README LICENSE
%{_bindir}/*
%{python_sitelib}/*


%changelog
* Tue Mar 12 2013 Satoru SATOH <ssato@redhat.com> - 0.2.5-1
- Initial packaging.
