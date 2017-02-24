# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname cbor
%global sumtxt  CBOR loader and dumper for Python
%global desctxt Concise Binary Object Representation (CBOR) is a superset of JSON's schema that's faster and more compact. This package provides python library provides loads()/dumps() like the json standard library.

Name:           python-%{pkgname}
Version:        1.0.0
Release:        1%{?dist}
Summary:        %{sumtxt}
Group:          Development/Libraries
License:        ASL 2.0
URL:            https://bitbucket.org/bodhisnarkva/cbor
Source0:        %{pkgname}-%{version}.tar.gz
# Available from https://github.com/brianolson/cbor_py.
#Source1:        README.md
#BuildArch:      noarch
BuildRequires:  python2-devel python3-devel
BuildRequires:  python-setuptools python3-setuptools

%description
%{desctxt}

%package     -n python2-%{pkgname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname}
%{desctxt}

%package     -n python3-%{pkgname}
Summary:        %{sumtxt}
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname}
%{desctxt}

%prep
%setup -q -n %{pkgname}-%{version}
cat << EOF > README.md
# From https://github.com/brianolson/cbor_py
Concise Binary Object Representation (CBOR) is a superset of JSON's schema
that's faster and more compact.

* http://tools.ietf.org/html/rfc7049
* http://cbor.io/

This Python implementation provides loads()/dumps() like the json standard
library.

Compare to Python 2.7.5's standard library implementation of json:

```
serialized 50000 objects into 1163097 cbor bytes in 0.05 seconds (1036613.48/s) and 1767001 json bytes in 0.22 seconds (224772.48/s)
compress to 999179 bytes cbor.gz and 1124500 bytes json.gz
load 50000 objects from cbor in 0.07 secs (763708.80/sec) and json in 0.32 (155348.97/sec)
```

There is also a pure-python implementation which gets about 1/3 the speed of
json's C augmented speed.
EOF


%build
%py3_build
%py2_build

%install
%py3_install
%py2_install

%files -n python2-%{pkgname}
%doc README.md
%{python2_sitearch}/*

%files -n python3-%{pkgname}
%doc README.md
%{python3_sitearch}/*

%changelog
* Fri Feb 24 2017 Satoru SATOH <ssato@redhat.com> - 1.0.0-1
- Initial packaging
