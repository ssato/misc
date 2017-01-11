%if 0%{?fedora}
%global with_python3 0%{!?_without_python3:1}
%endif

%global srcname dataset

%define _summary Toolkit for Python-based data processing
%define _desc Dataset makes reading and writing data in databases as simple as reading and writing JSON files.

Name:           python-%{srcname}
Version:        0.7.1
Release:        1%{?dist}
Summary:        %{_summary}
Group:          Development/Languages
License:        MIT
URL:            https://github.com/pudo/dataset
# From https://pypi.python.org/pypi/dataset
Source0:        %{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:       noarch
BuildRequires:  python2-devel
BuildRequires:  python3-devel
BuildRequires:  python-setuptools
BuildRequires:  python3-setuptools

%description
%{_desc}

%package -n     python2-%{srcname}
Summary:        %{_summary}
Requires:       python2-setuptools
Requires:       PyYAML
Requires:       python-alembic
Requires:       python-normality
Requires:       python-six
Requires:       python-sqlalchemy
%{?python_provide:%python_provide python2-dataset}

%description -n python2-%{srcname}
%{_desc}

%package -n     python3-%{srcname}
Summary:        %{_summary}
Requires:       python3-setuptools
Requires:       python3-PyYAML
Requires:       python3-alembic
Requires:       python3-normality
Requires:       python3-six
Requires:       python3-sqlalchemy
%{?python_provide:%python_provide python3-dataset}

%description -n python3-%{srcname}
%{_desc}

%prep
%setup -qn %{srcname}-%{version}

%build
%py3_build
%py2_build
# from https://github.com/pudo/dataset
cat << 'EOF' > README.md
dataset: databases for lazy people
==================================

In short, **dataset** makes reading and writing data in databases as simple as
reading and writing JSON files.

[Read the docs](https://dataset.readthedocs.io/)

To install dataset, fetch it with ``pip``:

```bash
$ pip install dataset
```
EOF

%install
%py3_install
rm -f bin.list
for f in $RPM_BUILD_ROOT%{_bindir}/*; do
    echo ${f} | sed "s,$RPM_BUILD_ROOT,,g" >> bin.list; mv $f $f-3
done
%py2_install

%check
# from .travis.yml
#export DATABASE_URL=sqlite:///:memory:
#export DATABASE_URL=postgresql+psycopg2://postgres@127.0.0.1/dataset
#export DATABASE_URL=mysql+pymysql://travis@127.0.0.1/dataset?charset=utf8
#psql -c 'DROP DATABASE IF EXISTS dataset;' -U postgres
#psql -c 'create database dataset;' -U postgres
#mysql -e 'create database IF NOT EXISTS dataset DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;'
#flake8 --ignore=E501,E123,E124,E126,E127,E128 dataset test
#nosetests

#pushd %{py3dir}
#...
#popd

%files -n       python2-%{srcname} -f bin.list
%doc README.md test
%{python2_sitelib}/*

%files -n       python3-%{srcname}
%doc README.md test
%{_bindir}/*-3
%{python3_sitelib}/*

%changelog
* Wed Jan 11 2017 Satoru SATOH <ssato@redhat.com> 0.7.1-1
- Initial RPM release.
