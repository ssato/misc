%global debug_package %{nil}

Name:           go
Version:        1.2
Release:        1%{?dist}
Summary:        The Go programming language compiler
Group:          Development/Languages
License:        BSD
URL:            http://golang.org
#Source0:       https://code.google.com/p/go/downloads/list
Source0:        %{name}%{version}.src.tar.gz
Patch0:         go-1.2_test_fixpath_hostname.patch
BuildRequires:  hostname

%description
Go is an open source programming language that makes it easy to build simple,
reliable, and efficient software.

%prep
%setup -q -n %{name}
%patch0 -p1 -b .fixpath

%build

%install
rm -rf $RPM_BUILD_ROOT

#export GOROOT_FINAL=$RPM_BUILD_ROOT%{_bindir}
export GOBIN=$RPM_BUILD_ROOT%{_bindir}
export GOOS=linux
export GOARCH=amd64
cd src
./all.bash

%files
%doc AUTHORS CONTRIBUTORS PATENTS README VERSION
%{_bindir}/*

%changelog
* Wed Jan 15 2014 Satoru SATOH <ssato@redhat.com> - 1.2-1
- Initial packaging.
