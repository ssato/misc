# To get the short commit ID in the git repo, run 'git rev-parse --short HEAD':
%global git_rev 597cca20eb
%global vimdir %{_datadir}/vim/vimfiles

Name:           nim-vim
Version:        0.1
Release:        1.%{git_rev}%{?dist}
Summary:        Vim syntax highlighting for Nim programming language
Group:          Applications/Editors
License:        Vim
URL:            https://github.com/zah/nim.vim
Source0:        https://github.com/zah/nim.vim/archive/master.zip
Requires:       vim-filesystem
BuildArch:      noarch

%description
This provides Nim language support for Vim, syntax highlighting, auto-indent,
build/jump to errors within Vim, project navigation and Jump to Definition
(cgats or compiler-assisted idetools).

The source of this script comes mainly from
http://www.vim.org/scripts/script.php?script_id=2632, which comes from a
modified python.vim (http://www.vim.org/scripts/script.php?script_id=790).

%prep
%setup -q -n nim.vim-master

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{vimdir}
for d in autoload compiler ftdetect ftplugin indent syntax; do
    cp -a $d $RPM_BUILD_ROOT%{vimdir}
done

%files
%doc README.markdown
%{vimdir}/*/*.*

%changelog
* Sun Aug 16 2015 Satoru SATOH - 0.1-1.git597cca20eb-1
- Initial package
