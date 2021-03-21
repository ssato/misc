Name:           shellspec
Version:        0.28.1
Release:        1%{?dist}
Summary:        A full-featured BDD unit testing framework for all POSIX shells
License:        MIT
URL:            https://shellspec.info/
Source0:        https://github.com/shellspec/%{name}/archive/refs/tags/%{version}.tar.gz
Requires:       bash
BuildArch:      noarch

%description
ShellSpec is a full-featured BDD unit testing framework for all POSIX shells
that provides first-class features such as code c overage, mocking,
parameterized test, parallel execution and more.

%global  pkglibdir %{_prefix}/lib/%{name}

%prep
%autosetup

%build
: # Nothing to do.

%install
%{make_install} PREFIX=%{buildroot}/usr

# Those should not to be installed.
rm -f %{buildroot}%{pkglibdir}/LICENSE

%check
:

%files
%doc *.md
%{_bindir}/*
%{pkglibdir}

%changelog
* Sun Mar 21 2021 Satoru SATOH <satoru.satoh@gmail.com> - 0.28.1-1
- initial packaging
