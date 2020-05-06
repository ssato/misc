# Ref. https://fedoraproject.org/wiki/Packaging:Python
%global pkgname smart_open
%global desctxt \
smart_open is a Python 2 & Python 3 library for efficient streaming of very \
large files from/to storages such as S3, HDFS, WebHDFS, HTTP, HTTPS, SFTP, or \
local filesystem. It supports transparent, on-the-fly (de-)compression for a \
variety of different formats. \
\
smart_open is a drop-in replacement for Python’s built-in open(): it can do \
anything open can (100% compatible, falls back to native open wherever \
possible), plus lots of nifty extra stuff on top.

Name:           python-%{pkgname}
Version:        2.0.0
Release:        1%{?dist}
Summary:        Library for efficient streaming of very large files from/to storages
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/RaRe-Technologies/smart_open
Source0:        %{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description %{desctxt}

# TODO: split aws and gcp support from the core package.
%package     -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-boto
Requires:       python3-boto3
Requires:       python3-google-cloud-storage
Requires:       python3-requests
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{desctxt}

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{pkgname}
%doc README.rst
# %%doc CHANGELOG.md MIGRATING_FROM_OLDER_VERSIONS.rst help.txt howto.md
%{python3_sitelib}/*

%changelog
* Wed May  6 2020 Satoru SATOH <satoru.satoh@gmail.com> - 2.0.0-1
- New upstream
- Add dependency to google-cloud-storage to support gcp

* Sat Nov 16 2019 Satoru SATOH <satoru.satoh@gmail.com> - 1.9.0-1
- Initial packaging
