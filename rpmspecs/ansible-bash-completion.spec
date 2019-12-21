%global orgname           ansible-completion
%global completiondir     /usr/share/bash-completion/completions/

%global commit            ad00a6d7850a50420b3febc6a4cc387184a1a5cc
%global commit_date       20191029
%global shortcommit       %(c=%{commit};echo ${c:0:7})
%global rel               1
%global gitrel            git%{rel}%{shortcommit}

Name:           ansible-bash-completion
# Upstream never released and this version, AFAIK.
Version:        %{commit_date}
Release:        %{gitrel}%{?dist}
Summary:        Bash completion support for ansible
License:        GPLv3
URL:            https://github.com/dysosmus/ansible-completion/
Source0:        %{url}/archive/master.zip
Requires:       ansible
Requires:       bash-completion
BuildArch:      noarch

%description
Ansible-completion provides a bash completion on host name, module name
and options for ansible.

%prep
%autosetup -n %{orgname}-master

%build
: # Nothing to do.

%install
install -d %{buildroot}%{completiondir}
for f in ansible*.bash; do install -m 644 $f %{buildroot}%{completiondir}/; done

%check
:

%files
%doc README*
%{completiondir}/ansible*.bash

%changelog
* Sat Dec 21 2019 Satoru SATOH <satoru.satoh@gmail.com> - 20191029-git1.ad00a6d
- initial packaging
