%global git_date_rev      201502241
%global nim_git_rev       d9370a2
%global csources_git_rev  96a5b7f

Name:           nim
Version:        0.11.2
#Release:        1.git.%{git_date_rev}%{?dist}
Release:        1
Summary:        Statically typed and imperative programming language
Group:          Development/Languages
License:        MIT
URL:            http://nim-lang.org
## Git version:
# Fetch git HEAD version and make an archive:
# git clone -b master git://github.com/Araq/Nim.git nim-%{git_date_rev} && \
#     rm -rf nim-%{git_date_rev}/.git* && \
#     tar --xz -cvf nim-%{git_date_rev}.tar.xz nim-%{git_date_rev}
#Source0:        %{name}-%{git_date_rev}.tar.xz
# Likewise:
# git clone -b master --depth 1 git://github.com/nim-lang/csources && \
#     rm -rf csources/.git* && \
#     tar --xz -cvf csources-%{git_date_rev}.tar.xz csources
#Source1:        csources-%{git_date_rev}.tar.xz
Source0:        http://nim-lang.org/download/%{name}-%{version}.tar.xz
Patch0:         nim-0.11.2-install-destdir.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#BuildRequires:  ...
Requires:       gcc

%description
Nim (formerly known as "Nimrod") is a statically typed, imperative programming
language that tries to give the programmer ultimate power without compromises
on runtime efficiency. This means it focuses on compile-time mechanisms in all
their various forms.

Beneath a nice infix/indentation based syntax with a powerful (AST based,
hygienic) macro system lies a semantic model that supports a soft realtime GC
on thread local heaps. Asynchronous message passing is used between threads, so
no "stop the world" mechanism is necessary. An unsafe shared memory heap is
also provided for the increased efficiency that results from that model.

%prep
#%setup -q -n %{name}-%{git_date_rev} -a1
%setup -q
%patch0 -p1 -b .destdir

%build
bash -x build.sh

%install
rm -rf %{buildroot}
bash -x install.sh /usr/bin %{buildroot}
mkdir -p %{buildroot}/etc/%{name}
test "x%{_libdir}" != x/usr/lib && mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
mv %{buildroot}/etc/nim*.* %{buildroot}/etc/%{name}/

%files
%defattr(-,root,root,-)
%doc readme.txt contributors.txt copying.txt
%doc examples doc web
%{_bindir}/*
#/usr/lib/%{name}
%{_libdir}/%{name}
%{_datadir}/%{name}
%config %{_sysconfdir}/%{name}/*

%changelog
* Sun Aug 16 2015 Satoru SATOH <ssato@redhat.com> - 0.11.2-1
- Initial package.
