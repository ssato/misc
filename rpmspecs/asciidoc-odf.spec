Name:           asciidoc-odf
Version:        0.1
Release:        1.git9f97a0dbe0%{?dist}
Summary:        ODF backend for AsciiDoc
License:        GPL+ and GPLv2+
URL:            https://github.com/LonoCloud/asciidoc-odf
Source0:        %{name}-%{version}.tar.xz
Patch0:         asciidoc-odf-filename-typo-in-Makefile.patch
BuildRequires:  python2-devel
BuildRequires:  asciidoc, /usr/bin/xmllint
Requires:       asciidoc

%description
The ODF backend for AsciiDoc enables AsciiDoc users to directly convert
documents from AsciiDoc to Open Document Format v1.2.

%prep
%setup -q -n %{name}.git
%patch0 -p1 -b.typo

%build
make DESTDIR=/ %{?_smp_mflags} link
#make DESTDIR=%{buildroot} %{?_smp_mflags} examples templates

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=%{buildroot} %{?_smp_mflags} install

%files
%doc examples README.asciidoc
%{_sysconfdir}/asciidoc/backends/od*/*
%{_sysconfdir}/asciidoc/themes/*/*.styles
%{_sysconfdir}/asciidoc/filters/code/*

%changelog
* Fri Aug 22 2014 Satoru SATOH <ssato@redhat.com> - 0.1-1.git9f97a0dbe0
- Switched the upstream git repo

* Thu Aug 21 2014 Satoru SATOH <ssato@redhat.com> - 0.1-1.git2fefe8b4ba
- Initial packaging. 
