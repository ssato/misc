%global debug_package %{nil}
%global _use_internal_dependency_generator 0
%global __find_requires /usr/lib/rpm/ocaml-find-requires.sh
%global __find_provides /usr/lib/rpm/ocaml-find-provides.sh
%global haxelibdir /usr/lib/haxe

Name:           haxe
Version:        3.0.1
Release:        1%{?dist}
Summary:        A multiplatform program language
License:        GPLv2+
URL:            http://haxe.org
#Source0:       https://github.com/HaxeFoundation/haxe/archive/v3.0.1.tar.gz
Source0:        %{name}-%{version}.tar.gz
# How to make:
#   git clone git://github.com/HaxeFoundation/ocamllibs.git && \
#   tar jcvf ocamllibs.tar.xz ocamllibs
Source1:        ocamllibs.tar.xz
BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-camlp4-devel
BuildRequires:  zlib-devel

%description
Haxe is a multiplatform program language with familiar syntax like Javascript
but strictly typed, and can be compiled to all popular programming platforms
with its fast compiler – JavaScript, Flash, NekoVM, PHP, C++, C# and Java –
which means your apps will support all popular mobile devices, such as iOS,
Android, Windows Mobile, webOS and more.

%prep
%setup -q -a 1
mv ocamllibs/* libs/

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
%{haxelibdir}/std

%changelog
* Mon Jan 13 2014 Satoru SATOH <ssato@redhat.com> - 3.0.1-1
- New upstream release
- Cleanup the RPM SPEC

* Tue Sep 10 2013 Satoru SATOH <ssato@redhat.com> - 3.0-1
- Initial packaging.
