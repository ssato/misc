%global vimfiles_root %{_datadir}/vim/vimfiles
%global appdata_dir %{_datadir}/appdata

Name:           vim-jinja
Version:        20190320
Release:        1%{?dist}
Summary:        Jinja2 syntax plugin for Vim
Group:          Applications/Editors
License:        Vim
URL:            http://www.vim.org/scripts/script.php?script_id=1856
Source0:        jinja.vim
BuildArch:      noarch
Requires:       vim-common
Requires(post): vim
Requires(postun): vim

%description
A Vim plugin that provides Jinja2 template file detection and syntax
highlighting.

%prep
%setup -Tc %{name}-%{version}
cp %{SOURCE0} ./

%build

%install
mkdir -p %{buildroot}%{vimfiles_root}/syntax
cp %{SOURCE0} %{buildroot}%{vimfiles_root}/syntax/

#%%post
#vim -c ":helptags %{vimfiles_root}/doc" -c ":q" &> /dev/null || :

#%%postun
#> %{vimfiles_root}/doc/tags || :
#vim -c ":helptags %{vimfiles_root}/doc" -c ":q" &> /dev/null || :

%files
%{vimfiles_root}/syntax/*

%changelog
* Mon Mar 20 2017 Satoru SATOH <ssato@redhat.com> - 20170320-1
- Initial package
