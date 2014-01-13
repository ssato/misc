# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%if 0%{?fedora}
%global with_python3 1
%endif

%define debug_package %{nil}
%define pymodname moss

Name:           python-%{pymodname}
Version:        0.2.0
Release:        1%{?dist}
Summary:        Python library for neroimaging and cognitive data analysis
License:        BSD
Group:          Development/Languages
URL:            https://github.com/mwaskom/moss
#Source0:        https://github.com/mwaskom/%{pymodname}/archive/v%{version}.tar.gz
Source0:        %{pymodname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-patsy
Requires:       python-pandas
Requires:       python-statsmodels
Requires:       python-scikit-learn
Requires:       python-six
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
Moss is a library of functions, classes, and scripts to that may be useful for
analyzing scientific data. Because this package is developed for neuroimaging
and cognitive science, there is probably some bias towards applications that
are useful in that domain. However, the functions are intended to be written in
as general and lightweight a fashion as possible.

%package        tools
Summary:        Misc tools for neroimaging and cognitive data analysis using %{name}
Requires:       %{name} = %{version}-%{release}

%description    tools
Moss is a library of functions, classes, and scripts to that may be useful for
analyzing scientific data. Because this package is developed for neuroimaging
and cognitive science, there is probably some bias towards applications that
are useful in that domain. However, the functions are intended to be written in
as general and lightweight a fashion as possible.

This package contains some scripts using python-%{pymodname}.

%if 0%{?with_python3}
%package -n     python3-%{pymodname}
Summary:        Python library for neroimaging and cognitive data analysis
Requires:       python3-patsy
Requires:       python3-pandas
Requires:       python3-statsmodels
Requires:       python3-scikit-learn
Requires:       python3-six

%description -n python3-%{pymodname}
Moss is a library of functions, classes, and scripts to that may be useful for
analyzing scientific data. Because this package is developed for neuroimaging
and cognitive science, there is probably some bias towards applications that
are useful in that domain. However, the functions are intended to be written in
as general and lightweight a fashion as possible.

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

%files          tools
%doc README.md
%{_bindir}/*

%if 0%{?with_python3}
%files -n       python3-%{pymodname}
%defattr(644,root,root,755)
%doc README.md
%{python3_sitelib}/*
%endif

%changelog
* Mon Jan 13 2014 Satoru SATOH <ssato@redhat.com> - 0.2.0-1
- Initial packaging
