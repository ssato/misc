# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%if 0%{?fedora}
%global with_python3 1
%endif

%define debug_package %{nil}
%define pymodname pyhusl

Name:           %{pymodname}
Version:        2.1.0
Release:        1%{?dist}
Summary:        A Python port of HUSL, human-friendly alternative to the HSL color space
License:        MIT
Group:          Development/Languages
URL:            https://github.com/boronine/pyhusl
#Source0:        https://github.com/boronine/pyhusl/archive/v%{version}.tar.gz
Source0:        %{pymodname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
A Python port of HUSL, a human-friendly alternative to the HSL color space. HSL
was designed back in the 70s to be computationally cheap. It is a clever
geometric transformation of the RGB color space and it does not take into
account the complexities of human color vision.

%if 0%{?with_python3}
%package -n     python3-%{pymodname}
Summary:        A Python port of HUSL, human-friendly alternative to the HSL color space

%description -n python3-%{pymodname}
A Python port of HUSL, a human-friendly alternative to the HSL color space. HSL
was designed back in the 70s to be computationally cheap. It is a clever
geometric transformation of the RGB color space and it does not take into
account the complexities of human color vision.

This is a package for python-3.
%endif

%prep
%setup -q -n %{pymodname}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif
 
%files
%doc README.md
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n       python3-%{pymodname}
%defattr(644,root,root,755)
%doc README.md
%{python3_sitelib}/*
%endif

%changelog
* Sun Jan 12 2014 Satoru SATOH <ssato@redhat.com> - 2.1.0-1
- Initial packaging
