%global pkgname git-url-parse
%global desctxt \
A simple GIT URL parser similar to giturlparse.py

Name:           python-%{pkgname}
Version:        1.2.2
Release:        2%{?dist}
Summary:        A simple GIT URL parser
License:        MIT
URL:            https://github.com/coala/git-url-parse
Source0:        %{url}/archive/RELEASE_%{version}.tar.gz
Patch0:         git-url-parse-1.2.2-disable-pbr.patch
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description   %desctxt

%package     -n python3-%{pkgname}
Summary:        %{summary}
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

* Sun Sep 29 2019 Satoru SATOH <satoru.satoh@gmail.com> - 1.2.2-1
- Initial packaging
