%global vimfiles_root %{_datadir}/vim/vimfiles

Name:           ansible-vim
Summary:        Ansible support plugin for vim
Version:        1.0
Release:        1%{?dist}
Group:          Applications/Editors
License:        MIT
URL:            https://github.com/pearofducks/ansible-vim
#Source0:        https://github.com/pearofducks/ansible-vim/archive/1.0.tar.gz
Source0:        %{name}-%{version}.tar.gz
Requires:       vim-common
BuildArch:      noarch

%description
Ansible support plugin for vim.

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}/%{vimfiles_root}
cp -ar {ftdetect,ftplugin,indent,syntax} %{buildroot}%{vimfiles_root}

%files 
%{vimfiles_root}/*/*.*
%doc README.md

%changelog
* Mon Mar 27 2017 Satoru SATOH <satoru.satoh@gmail.com> - 1.0-1
- Initial packaging
