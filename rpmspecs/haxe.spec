%global debug_package %{nil}
%global _use_internal_dependency_generator 0
%global __find_requires /usr/lib/rpm/ocaml-find-requires.sh
%global __find_provides /usr/lib/rpm/ocaml-find-provides.sh

Name:           haxe
Version:        3.0
Release:        1%{?dist}
Summary:        A multiplatform program language
License:        GPLv2+
URL:            http://haxe.org
## How to make:
# svn co http://haxe.googlecode.com/svn/tags/v3-00/ haxe-3.0 && \
#     tar --xz -cvf haxe-3.0.tar.xz
Source0:        %{name}-%{version}.tar.xz
Patch0:         haxe-Makefile-libdir.patch
BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-camlp4-devel
BuildRequires:  subversion
BuildRequires:  zlib-devel


%description
Haxe is a multiplatform program language with familiar syntax like Javascript
but strictly typed, and can be compiled to all popular programming platforms
with its fast compiler – JavaScript, Flash, NekoVM, PHP, C++, C# and Java –
which means your apps will support all popular mobile devices, such as iOS,
Android, Windows Mobile, webOS and more.


%prep
%setup -q
%patch0 -p1 -b.libdir


%build
make clean all


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/haxe/{std,lib}
make install INSTALL_DIR=$RPM_BUILD_ROOT/usr LIBDIR=$RPM_BUILD_ROOT%{_libdir}


%files
%doc doc
%{_bindir}/*
%{_libdir}/haxe/std
%{_libdir}/haxe/lib


%changelog
* Tue Sep 10 2013 Satoru SATOH <ssato@redhat.com> - 3.0-1
- Initial packaging.
