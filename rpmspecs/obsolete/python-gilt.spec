%global pkgname gilt
%global desctxt \
Gilt is a GIT layering tool to overlay a remote repository into the \
destination provided.

Name:           python-%{pkgname}
Version:        1.2.1
Release:        2%{?dist}
Summary:        A GIT layering tool
License:        MIT
URL:            https://github.com/metacloud/gilt/
Source0:        %{url}/archive/RELEASE_%{version}.tar.gz
# pbr brings many troubles so I want to disable it.
Patch0:         gilt-1.2.1-disable-pbr.patch
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description   %desctxt

%package     -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-click
Requires:       python3-colorama
Requires:       python3-fasteners
Requires:       python3-pyyaml
# It's not in Fedora repo but available from my copr repo,
# https://copr.fedorainfracloud.org/coprs/ssato/extras/
Requires:       python3-git-url-parse
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desctxt}

%prep
%autosetup -n %{pkgname}-%{version} -p1

%build
%py3_build

%install
%py3_install

%files -n python3-%{pkgname}
%doc *.rst
%{python3_sitelib}/*

%changelog
* Sun Sep 29 2019 Satoru SATOH <satoru.satoh@gmail.com> - 1.2.2-2
- fix summary text

* Sun Sep 29 2019 Satoru SATOH <satoru.satoh@gmail.com> - 1.2.1-1
- Initial packaging
