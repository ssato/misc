# This is my fork version originally came from Fedora.
%global pkgname molecule
%global setup_flags SKIP_PIP_INSTALL=1 PBR_VERSION=%{version}
%global desctxt \
Molecule is designed to aid in the development and testing of Ansible roles. \
Molecule provides support for testing with multiple instances, operating \
systems and distributions, virtualization providers, test frameworks and \
testing scenarios. Molecule is opinionated in order to encourage an approach \
that results in consistently developed roles that are well-written, easily \
understood and maintained. Molecule uses Ansible playbooks to exercise the \
role and its associated tests. Molecule supports any provider that Ansible \
supports.

%{?python_disable_dependency_generator}

Name: python-%{pkgname}
Version: 3.0a4
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
#Patch0: molecule-2.20.2_missing-data.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1685311
#Patch1: molecule-2.20.2_frozen-ver.patch
#Patch2: molecule-2.20.2_pytest-3.patch
Patch10: molecule-3.0a3-include-data_files.patch

BuildArch: noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# https://github.com/ansible/molecule/blob/master/setup.cfg
BuildRequires:  python3-setuptools_scm >= 1.15.0
BuildRequires:  python3-setuptools_scm_git_archive >= 1.0
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx_rtd_theme

%description    %desctxt

%package     -n python-molecule-doc
Summary: %summary
%description -n python-molecule-doc
Documentation for python-molecule

%package     -n python3-molecule
Summary: %summary
Recommends: python-%{pkgname}-doc = %{version}-%{release}
Recommends: python3-docker
# https://bugzilla.redhat.com/show_bug.cgi?id=1614358
# https://github.com/ansible/molecule/blob/master/setup.cfg
Requires: ansible
Requires: python3-ansible-lint >= 4.0.2
Requires: python3-anyconfig >= 0.9.10
Requires: python3-flake8 >= 3.6.0
Requires: python3-cerberus >= 1.3.1
Requires: python3-click >= 7.0
Requires: python3-click-completion >= 0.5.1
Requires: python3-colorama >= 0.3.9
Requires: python3-cookiecutter >= 1.6.0
Requires: python3-jinja2 >= 2.10.1
Requires: python3-paramiko >= 2.5.0
Requires: python3-pexpect >= 4.6
Requires: python3-pluggy >= 0.7.1
Requires: python3-pyyaml >= 5.1
Requires: python3-sh >= 1.12.14
Requires: python3-six >= 1.11.0
Requires: python3-tabulate >= 0.8.4
Requires: python3-testinfra >= 3.0.6
Requires: python3-tree-format >= 0.1.2
Requires: yamllint >= 1.15.0
# These're not in Fedora repo but available from my copr repo,
# https://copr.fedorainfracloud.org/coprs/ssato/extras/.
Requires: python3-gilt >= 1.2.1
Requires: python3-pre-commit >= 1.17.0
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-molecule %desctxt

%prep
%autosetup -n %{pkgname}-%{version} -p1

%build
%{setup_flags} %{py3_build}

# generate html docs
(
cd docs
PYTHONPATH=.. sphinx-build-3 ./ html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
)

%install
%{setup_flags} %{py3_install}

# Dirty Hack for https://github.com/ansible/molecule/issues/1851
install -d %{buildroot}/%{python3_sitelib}/molecule/provisioner/ansible/plugins/{filter,modules}/
for f in molecule/provisioner/ansible/plugins/filter/*.py; do
  install -m 644 $f %{buildroot}/%{python3_sitelib}/molecule/provisioner/ansible/plugins/filter/
done
for f in molecule/provisioner/ansible/plugins/modules/*.py; do
  install -m 644 $f %{buildroot}/%{python3_sitelib}/molecule/provisioner/ansible/plugins/modules/
done

%check
# FIXME: library pathing issues causing tests to fail
# X{setup_flags} X{__python3} setup.py test

%files -n python3-molecule
%license LICENSE
%{python3_sitelib}/*
%{_bindir}/*

%files -n python-molecule-doc
%license LICENSE
%doc docs/html

%changelog
* Fri Nov 08 2019 Satoru SATOH <satoru.satoh@gmail.com> - 3.0a4-1
- New upstream pre-release
- change dependency to ansible instead of ansible-python3 to avoid conflicts

* Sun Oct 06 2019 Satoru SATOH <satoru.satoh@gmail.com> - 3.0a3-2
- Workaround for https://github.com/ansible/molecule/issues/1851
- Workaround that python-pexpect == 4.6.0 is not available but 4.6

* Sun Sep 29 2019 Satoru SATOH <satoru.satoh@gmail.com> - 3.0a3-1
- update to 3.0a3

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
