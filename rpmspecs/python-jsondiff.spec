# SEEALSO:
# - https://fedoraproject.org/wiki/Packaging:Python
# - https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/
#
%global srcname jsondiff
%global desctxt \
Diff JSON and JSON-like structures in Python.

Name:           python-%{srcname}
Version:        1.2.0
Release:        3%{?dist}
Summary:        Python library diffs JSON and JSON-like structures
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/fzumstein/jsondiff
Source0:        %pypi_source
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description    %{desctxt}

%package     -n python3-%{srcname}
Summary:        %{summary}
%py_provides python3-%{srcname}

%description -n python3-%{srcname} %{desctxt}

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{srcname}
%doc README.rst
%doc README.rst
%{python3_sitelib}/*
%{_bindir}/*diff

%changelog
* Thu May 11 2021 Satoru SATOH <satoru.satoh@gmail.com> - 1.2.0-3
- Refactoring

* Wed May  6 2020 Satoru SATOH <satoru.satoh@gmail.com> - 1.2.0-2
- Drop py2 support

* Mon Feb 24 2020 Satoru SATOH <satoru.satoh@gmail.com> - 1.2.0-1
- Initial packaging
