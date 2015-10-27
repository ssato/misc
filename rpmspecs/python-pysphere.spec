# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname pysphere
%global srcname %{pkgname}
%global sumtxt  Python API for interacting with the vSphere Web Services SDK
%global desc    Python API for interacting with the vSphere Web Services SDK.
# I'm not sure that pysphere works with python3.
%global with_python3 0

Name:           python-%{pkgname}
Version:        0.1.8
Release:        1%{?dist}
Summary:        %{sumtxt}
Group:          Development/Libraries
License:        BSD
#URL:            https://github.com/argos83/%{srcname}
URL:            https://pysphere.googlecode.com/files/%{srcname}-%{version}.zip
Source0:        %{srcname}-%{version}.zip
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
%{desc}

%package     -n python2-%{pkgname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{pkgname}
%{desc}

%if 0%{?with_python3}
%package     -n python3-%{pkgname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{pkgname}
%{desc}
%endif

%prep
%setup -q -n %{srcname}-%{version}
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
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%files -n python2-%{pkgname}
%doc README
%{python2_sitelib}/*

%if 0%{?with_python3}
%files -n python3-%{pkgname}
%doc README
%{python3_sitelib}/*
%endif

%changelog
* Fri Oct 16 2015 Satoru SATOH <ssato@redhat.com> - 0.1.8-1
- Initial packaging
