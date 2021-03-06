# TODO: build i386 RPMs.

%global debug_package %{nil}
%global pkglibexecdir %{_libexecdir}/go

Name:           go
Version:        1.2
Release:        1%{?dist}
Summary:        The Go programming language compiler
Group:          Development/Languages
License:        BSD
URL:            http://golang.org
#Source0:       https://code.google.com/p/go/downloads/list
Source0:        %{name}%{version}.src.tar.gz
%if 0%{?fedora}
Patch0:         go-1.2_test_fixpath_hostname.patch
BuildRequires:  hostname
%else
BuildRequires:  net-tools
%endif

%description
Go is an open source programming language that makes it easy to build simple,
reliable, and efficient software.

%prep
%setup -q -n %{name}
%if 0%{?fedora}
%patch0 -p1 -b .fixpath
%endif

%build

%install
rm -rf $RPM_BUILD_ROOT

# see: http://golang.org/doc/install/source#environmen
export GOROOT=$RPM_BUILD_ROOT/%{pkglibexecdir}
export GOBIN=$GOROOT
export GOOS=linux
cd src
./all.bash

# make up an wrapper:
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cat << "EOF" > $RPM_BUILD_ROOT%{_bindir}/go
#! /bin/bash
ncpus=$(( $(sed -ne 's/^processor.*/1 + /p;' /proc/cpuinfo) + 0))

GOMAXPROCS=${GOMAXPROCS:-${ncpus}} GOROOT=%{pkglibexecdir} \
  %{pkglibexecdir}/go $@
EOF
chmod +x $RPM_BUILD_ROOT%{_bindir}/go

%files
%doc AUTHORS CONTRIBUTORS PATENTS README VERSION
%{_bindir}/*
%{pkglibexecdir}/*

%changelog
* Thu Jan 16 2014 Satoru SATOH <ssato@redhat.com> - 1.2-1
- Initial packaging.
