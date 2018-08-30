%global srcname Vim-Jinja2-Syntax
%global vimfiles_root %{_datadir}/vim/vimfiles

Name:           vim-jinja2-syntax
Version:        20180830
Release:        1%{?dist}
Summary:        An up-to-date jinja2 syntax file for vim
License:        Vim
URL:            https://github.com/Glench/Vim-Jinja2-Syntax
Source0:        %{url}/archive/master.zip
Requires:       vim-common
BuildArch:      noarch
#Requires(post): vim
#Requires(postun): vim

%description
This is the latest version of the Jinja2 syntax file for vim with the ability
to detect either HTML or Jinja.

%prep
%setup -qn %{srcname}-master

%build

%install
mkdir -p %{buildroot}%{vimfiles_root}
cp -ar [a-z]*/ %{buildroot}%{vimfiles_root}

#%%post
#vim -c ":helptags %{vimfiles_root}/doc" -c ":q" &> /dev/null || :

#%%postun
#> %{vimfiles_root}/doc/tags || :
#vim -c ":helptags %{vimfiles_root}/doc" -c ":q" &> /dev/null || :

%files
%doc README.md
%{vimfiles_root}/ftdetect/*
%{vimfiles_root}/indent/*
%{vimfiles_root}/syntax/*

%changelog
* Thu Aug 30 2018 Satoru SATOH <ssato@redhat.com> - 20180830-1
- Initial package
