# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname avro
%global sumtxt Python module for Apache Avro serialization system
%global desctxt \
Apache Avro is a data serialization and RPC framework and this is a python\
package to [de]serialize Avro data.

Name:           python2-%{pkgname}
Version:        1.8.2
Release:        1%{?dist}
Summary:        %{sumtxt}
Group:          Development/Libraries
License:        ASL 2.0
URL:            http://avro.apache.org
Source0:        %{pkgname}-%{version}.tar.gz

BuildArch:      noarch
%if 0%{?rhel} == 7
BuildRequires:  python-devel
BuildRequires:  python-setuptools
%else
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%endif

%description    %{desctxt}

%prep
%autosetup -n %{pkgname}-%{version}

# Fix a problem (shebung in python modules) in the upstream w/ quich hack.
sed -i '/#!.*/d' src/avro/*.py

# Upsteam does not provide any doc..
cat << EOF > README.Fedora
%{desctxt}

- website: http://avro.apache.org
- doc: https://avro.apache.org/docs/1.8.2/gettingstartedpython.html
EOF

%build
%py2_build

%install
%py2_install
mv %{buildroot}%{_bindir}/avro %{buildroot}%{_bindir}/avro-2

%files
%doc README.Fedora
%{_bindir}/avro-2
%if 0%{?rhel} == 7
%{python_sitelib}/*
%else
%{python2_sitelib}/*
%endif

%changelog
* Mon Jan  8 2018 Satoru SATOH <ssato@redhat.com> - 1.8.2-1
- Initial packaging
