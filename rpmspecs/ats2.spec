%global arcname ATS2-Postiats
%global debug_package %{nil}
%global includedir %{_prefix}/include

Name:           ats2
Version:        0.0.8
Release:        1%{?dist}
Summary:        Programming language with advanced type systems
License:        GPLv3
URL:            http://www.ats-lang.org
#Source0:       http://sourceforge.net/projects/ats2-lang/files/
Source0:        %{arcname}-%{version}.tgz
Source1:        %{arcname}-include-%{version}.tgz
Source2:        %{arcname}-contrib-%{version}.tgz
BuildRequires:  gmp-devel

%description
ATS (Applied Type System) is a programming language whose stated purpose is to
support theorem proving in combination with practical programming through the
use of advanced type systems.[1] The performance of ATS has been demonstrated
to be comparable to that of the C and C++ programming languages.[2] By using
theorem proving and strict type checking, the compiler can detect and prove
that its implemented functions are not susceptible to bugs such as division by
zero, memory leaks, buffer overflow, and other forms of memory corruption by
verifying pointer arithmetic and reference counting before the program
compiles. Additionally, by using the integrated theorem-proving system of ATS
(ATS/LF), the programmer may make use of static constructs that are intertwined
with the operative code to prove that a function attains its specification.
[from http://en.wikipedia.org/wiki/ATS_%28programming_language%29)

%package        devel
Summary:        Development files for %{name}
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Development files for %{name}.

%prep
%setup -q -n %{arcname}-%{version} -a 1 -a 2

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{includedir}
cp -a %{arcname}-include-%{version} $RPM_BUILD_ROOT%{includedir}/ats2-postiats-%{version}
cp -a %{arcname}-contrib-%{version}/contrib $RPM_BUILD_ROOT%{includedir}/ats2-postiats-%{version}/
cp -a %{arcname}-contrib-%{version}/document ./contrib_document
#rm -f $RPM_BUILD_ROOT%{_includeddir}/ats2-postiats-%{version}/{COPYING,README}

%files
%doc RELEASE/
%{_bindir}/*
%{_prefix}/lib*/ats2-postiats-%{version}

%files          devel
%doc contrib_document
%{includedir}/*

%changelog
* Sat Jun  7 2014 Satoru SATOH <ssato@redhat.com> - 0.0.8-1
- Initial packaging.
