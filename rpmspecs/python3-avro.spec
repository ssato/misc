# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname avro
%global srcname avro-python3
%global sumtxt Python module for Apache Avro serialization system
%global desctxt \
Apache Avro is a data serialization and RPC framework and this is a python\
package to [de]serialize Avro data.

Name:           python3-%{pkgname}
Version:        1.8.2
Release:        1%{?dist}
Summary:        %{sumtxt}
Group:          Development/Libraries
License:        ASL 2.0
URL:            http://avro.apache.org
Source0:        %{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description    %{desctxt}

%prep
%autosetup -n %{srcname}-%{version}

# Fix a problem (shebung in python modules) in the upstream w/ quich hack.
sed -i '/#!.*/d' avro/*.py

%build
%py3_build

%install
%py3_install
mv %{buildroot}%{_bindir}/avro %{buildroot}%{_bindir}/avro-3

%files
%doc README.txt
%{_bindir}/avro-3
%{python3_sitelib}/*

%changelog
* Mon Jan  8 2018 Satoru SATOH <ssato@redhat.com> - 1.8.2-1
- Initial packaging
