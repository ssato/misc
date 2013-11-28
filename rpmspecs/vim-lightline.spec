%global vimfiles_root %{_datadir}/vim/vimfiles
%global pname lightline
%global commit add73a2

Name:           vim-%{pname}
Summary:        A light and configurable statusline/tabline for Vim
Version:        0.0.0
Release:        1.%{commit}git%{?dist}
Group:          Applications/Editors
License:        MIT
URL:            http://github.com/itchyny/lightline.vim
# You need to make up the archive by yourself from git cloned src tree.
Source0:        lightline.vim.tar.xz
Requires:       vim-common
Requires(post): vim
Requires(postun): vim
BuildArch:      noarch

%description
A light and configurable statusline/tabline for Vim

%prep
%setup -q -n lightline.vim

%build

%install
mkdir -p %{buildroot}/%{vimfiles_root}
cp -ar {autoload,doc,plugin} %{buildroot}%{vimfiles_root}
chmod 644 %{buildroot}%{vimfiles_root}/doc/*

%post
vim -c ":helplightline %{vimfiles_root}/doc" -c :q &> /dev/null

%postun
rm %{vimfiles_root}/doc/tags
vim -c ":helplightline %{vimfiles_root}/doc" -c :q &> /dev/null

%clean

%files 
%{vimfiles_root}/plugin/*.vim
%{vimfiles_root}/autoload/lightline.vim
%{vimfiles_root}/autoload/lightline/*.vim
%{vimfiles_root}/autoload/lightline/colorscheme/*.vim
%doc %{vimfiles_root}/doc/*
%doc README.md

%changelog
* Thu Nov 28 2013 Satoru SATOH <satoru.satoh@gmail.com> - 0.0.0-1.add73a2git
- Initial version
