# This is my fork version originally came from Fedora.
%global pkgname testinfra
%global setup_flags SKIP_PIP_INSTALL=1 PBR_VERSION=%{version}

Name:           python-%{pkgname}
Version:        3.0.5
Release:        1%{?dist}
Summary:        Unit testing for config-managed server state

License:        ASL 2.0
URL:            https://github.com/philpep/%{pkgname}
Source0:        %{url}/archive/%{version}/%{pkgname}-%{version}.tar.gz

Patch0:         testinfra-3.0.5_disable_setuptools_scm.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr

# testing requirements
BuildRequires:  ansible
BuildRequires:  python3-mock
BuildRequires:  python3-six
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-xdist
BuildRequires:  python3-pytest-cov
BuildRequires:  python3-winrm
BuildRequires:  python3-paramiko
BuildRequires:  python3-setuptools_scm

# docs requirements
BuildRequires:  python3-sphinx


%description
With Testinfra you can write unit tests in Python to test actual state of your
servers configured by management tools like Salt, Ansible, Puppet, Chef and so
on.

Testinfra aims to be a Serverspec equivalent in python and is written as a
plugin to the powerful Pytest test engine

%package     -n python3-%{pkgname}
Summary:        Unit testing for config-managed server state
Requires:  python3-pbr
Requires:  python3-mock
Requires:  python3-six
Requires:  python3-pytest
Requires:  python3-pytest-xdist
Requires:  python3-pytest-cov
Requires:  python3-winrm
Requires:  python3-paramiko
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname}
With Testinfra you can write unit tests in Python to test actual state of your
servers configured by management tools like Salt, Ansible, Puppet, Chef and so
on.

Testinfra aims to be a Serverspec equivalent in python and is written as a
plugin to the powerful Pytest test engine



%prep
%autosetup -n %{pkgname}-%{version}

# no Python 3 salt
rm testinfra/backend/salt.py
sed -i "/'salt':/d" testinfra/backend/__init__.py

%build
%setup_flags %py3_build

# generate html docs
sphinx-build-3 doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}


%install
%setup_flags %py3_install


%check
# majority of the tests gets skipped without docker, but some run
%{__python3} -m pytest test

%files -n python3-%{pkgname}
%license LICENSE
%doc html *.rst
# %%{_bindir}/%%{pkgname}
%{python3_sitelib}/%{pkgname}
%{python3_sitelib}/%{pkgname}-%{version}-py?.?.egg-info


%changelog
* Thu Jul 18 2019 Satoru SATOH <ssato@redhat.com> - 3.0.5-1
- update to 3.0.5
- remove testinfra command

* Tue Feb 05 2019 Miro Hrončok <mhroncok@redhat.com>
- Drop Python 2 subpackage

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 23 2018 Brett Lentz <brett.lentz@gmail.com> - 1.17.0-1
- update version

* Tue Jul 17 2018 Brett Lentz <brett.lentz@gmail.com> - 1.14.0-1
- update version

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.12.0-3
- Rebuilt for Python 3.7

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.12.0-2
- Rebuilt for Python 3.7

* Tue May 1 2018 Brett Lentz <brett.lentz@gmail.com> - 1.12.0-1
- update version

* Tue Apr 3 2018 Brett Lentz <brett.lentz@gmail.com> - 1.11.1-2
- fix deps

* Tue Mar 6 2018 Brett Lentz <brett.lentz@gmail.com> - 1.11.1-1
- update version

* Wed Jan 24 2018 Brett Lentz <brett.lentz@gmail.com> - 1.10.1-1
- initial package
