# This is my fork version originally came from Fedora.
%global pkgname molecule
%global setup_flags SKIP_PIP_INSTALL=1 PBR_VERSION=%{version}

%{?python_disable_dependency_generator}

Name: python-molecule
Version: 2.20.2
Release: 1%{?dist}
Summary: Molecule is designed to aid in the development and testing of Ansible roles

# Most of the package is MIT licensed.
#
# There are two files in the archive that are licensed with ASL 2.0:
# - molecule-2.7/molecule/interpolation.py
# - molecule-2.7/test/unit/test_interpolation.py
License: MIT and ASL 2.0

URL: https://github.com/metacloud/molecule
Source0: https://github.com/metacloud/molecule/archive/%{version}.tar.gz

# https://bugzilla.redhat.com/show_bug.cgi?id=1653467
Patch0: molecule-2.20.2_missing-data.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1685311
Patch1: molecule-2.20.2_frozen-ver.patch
Patch2: molecule-2.20.2_pytest-3.patch

BuildArch: noarch
BuildRequires:  yamllint
BuildRequires:  python3-anyconfig
BuildRequires:  python3-cerberus
BuildRequires:  python3-click
BuildRequires:  python3-colorama
BuildRequires:  python3-cookiecutter
BuildRequires:  python3-devel
BuildRequires:  python3-jinja2
BuildRequires:  python3-marshmallow
BuildRequires:  python3-PyYAML
BuildRequires:  python3-pexpect
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  python3-sh
BuildRequires:  python3-sphinx
BuildRequires:  python3-tabulate
BuildRequires:  python3-tree-format

%description
Molecule is designed to aid in the development and testing of Ansible roles.
Molecule provides support for testing with multiple instances, operating
systems and distributions, virtualization providers, test frameworks and
testing scenarios. Molecule is opinionated in order to encourage an approach
that results in consistently developed roles that are well-written, easily
understood and maintained. Molecule uses Ansible playbooks to exercise the role
and its associated tests. Molecule supports any provider that Ansible supports.

%package     -n python-molecule-doc
Summary: %summary
%description -n python-molecule-doc
Documentation for python-molecule

%package     -n python3-molecule
Summary: %summary
Recommends: python-molecule-doc
Recommends: python3-docker
# https://bugzilla.redhat.com/show_bug.cgi?id=1614358
Recommends: yamllint
Recommends: python3-ansible-lint
Requires: ansible-python3
Requires: python3-anyconfig
Requires: python3-cerberus
Requires: python3-click
Requires: python3-click-completion
Requires: python3-colorama
Requires: python3-cookiecutter
Requires: python3-flake8
Requires: python3-future
Requires: python3-jinja2
Requires: python3-marshmallow
Requires: python3-PyYAML
Requires: python3-pbr
Requires: python3-pexpect
Requires: python3-poyo
Requires: python3-requests
Requires: python3-sh
Requires: python3-tabulate
Requires: python3-testinfra
Requires: python3-tree-format
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-molecule
Molecule is designed to aid in the development and testing of Ansible roles.
Molecule provides support for testing with multiple instances, operating
systems and distributions, virtualization providers, test frameworks and
testing scenarios. Molecule is opinionated in order to encourage an approach
that results in consistently developed roles that are well-written, easily
understood and maintained. Molecule uses Ansible playbooks to exercise the role
and its associated tests. Molecule supports any provider that Ansible supports.


%prep
%autosetup -n %{pkgname}-%{version} -p1
cat <<EOF >> setup.cfg

[files]
data_files =
    %{python3_sitelib}/%{pkgname}/cookiecutter = molecule/cookiecutter/*
EOF

%build
%{setup_flags} %{py3_build}


# generate html docs
PYTHONPATH=. sphinx-build-3 doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%{setup_flags} %{py3_install}

%check
# FIXME: library pathing issues causing tests to fail
# X{setup_flags} X{__python3} setup.py test

%files -n python3-molecule
%license LICENSE
%{python3_sitelib}/*
%{_bindir}/%{pkgname}

%files -n python-molecule-doc
%license LICENSE
%doc doc
%doc *.rst
%doc *-requirements.txt

%changelog
* Thu Jun 27 2019 Satoru SATOH <ssato@redhat.com> - 2.20.2-1
- update to 2.20.2
- apply some patches to make it work

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 23 2018 Brett Lentz <brett.lentz@gmail.com> - 2.19-1
- update to 2.19

* Thu Oct 11 2018 Miro Hrončok <mhroncok@redhat.com> - 2.16-2
- Python2 binary package has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Tue Jul 17 2018 Brett Lentz <brett.lentz@gmail.com> - 2.16-1
- update to 2.16

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.13.1-3
- Rebuilt for Python 3.7

* Fri May 11 2018 Brett Lentz <brett.lentz@gmail.com> - 2.13.1-2
- add Recommends for default use case

* Wed May 9 2018 Brett Lentz <brett.lentz@gmail.com> - 2.13.1-1
- update to 2.13.1
- ensure all needed files are installed

* Mon Apr 30 2018 Brett Lentz <brett.lentz@gmail.com> - 2.13-1
- update to 2.13

* Mon Apr 2 2018 Brett Lentz <brett.lentz@gmail.com> - 2.12.1-2
- update to 2.12.1

* Thu Mar 29 2018 Brett Lentz <brett.lentz@gmail.com> - 2.11-1
- update to 2.11

* Wed Mar 14 2018 Brett Lentz <brett.lentz@gmail.com> - 2.10.1-3
- fix package deps

* Mon Mar 12 2018 Brett Lentz <brett.lentz@gmail.com> - 2.10.1-1
- update to 2.10.1

* Mon Mar 5 2018 Brett Lentz <brett.lentz@gmail.com> - 2.9-1
- update to 2.9

* Tue Jan 23 2018 Brett Lentz <brett.lentz@gmail.com> - 2.7-1
- initial package
