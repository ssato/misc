# borrowed from http://pkgs.fedoraproject.org/cgit/rpms/rust.git/tree/rust.spec
%global rust_arches x86_64 i686 armv7hl aarch64 ppc64 ppc64le s390x

%global vimfiles_root %{_datadir}/vim/vimfiles
%global appdata_dir %{_datadir}/appdata

Name:           vim-rust
Version:        20170106
Release:        1%{?dist}
Summary:        Rust development plugin for Vim
Group:          Applications/Editors
License:        ASL 2.0 or MIT
URL:            https://github.com/rust-lang/rust.vim
Source0:        https://github.com/rust-lang/rust.vim/archive/master.zip
Source1:        %{name}.metainfo.xml
# Fedora => noarch, the rest arch-specific
%if 0%{?fedora}
BuildArch:      noarch
%endif
ExclusiveArch:  %{rust_arches}
Requires:       vim-common
Requires(post): vim
Requires(postun): vim
Requires:       rust

%description
A Vim plugin that provides Rust file detection, syntax highlighting,
formatting, Syntastic integration, and more.

%package -n     vim-syntastic-rust
Summary:        A syntax checker for Rust programming language
Group:          Applications/Editors
Requires:       vim-syntastic

%description -n vim-syntastic-rust
A syntax checker for Rust programming language.

%prep
%setup -qn rust.vim-master

%build

%install
mkdir -p %{buildroot}%{vimfiles_root}
cp -ar [a-z]*/ %{buildroot}%{vimfiles_root}

mkdir -p %{buildroot}%{appdata_dir}
install -m 644 %{SOURCE1} %{buildroot}%{appdata_dir}

%post
vim -c ":helptags %{vimfiles_root}/doc" -c ":q" &> /dev/null || :

%postun
> %{vimfiles_root}/doc/tags || :
vim -c ":helptags %{vimfiles_root}/doc" -c ":q" &> /dev/null || :

%files
%license LICENSE-{APACHE,MIT}
%doc README.md
%{vimfiles_root}/after/*
%{vimfiles_root}/autoload/*
%{vimfiles_root}/compiler/*
%{vimfiles_root}/doc/*
%{vimfiles_root}/ftdetect/*
%{vimfiles_root}/ftplugin/*
%{vimfiles_root}/indent/*
%{vimfiles_root}/plugin/*
%{vimfiles_root}/syntax/*
%{appdata_dir}/%{name}.metainfo.xml

%files -n       vim-syntastic-rust
%license LICENSE-{APACHE,MIT}
%doc README.md
%{vimfiles_root}/syntax_checkers/*

%changelog
* Fri Jan  6 2017 Satoru SATOH <ssato@redhat.com> - 20170106-1
- Initial package
