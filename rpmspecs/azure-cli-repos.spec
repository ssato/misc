Summary:        Azure CLI package repositories
Name:           azure-cli-repos
Version:        1.0
Release:        1%{?dist}
License:        MIT
Group:          System Environment/Base
URL:            https://github.com/Azure/azure-cli/
# How to make this archive:
# 0. Create source dir: mkdir azure-cli-repos-1.0
# 1. Download GPG public key and save it as RPM-GPG-microsoft-azure-cli (or
#    whatever appropriate name such like other ones in /etc/pki/rpm-gpg/)
#    and put it into the source dir.
#    
#    - GPG public key: https://packages.microsoft.com/keys/microsoft.asc
#
# 2. Create the yum .repo file:
#
# cat << EOF > azure-cli-repos-1.0/azure-cli.repo 
# [azure-cli]
# name=Azure CLI
# baseurl=https://packages.microsoft.com/yumrepos/azure-cli
# #gpgkey=https://packages.microsoft.com/keys/microsoft.asc
# gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-microsoft-azure-cli
# gpgcheck=1
# enabled=1
# EOF
# 
# 3. Create the archive: tar --xz -cvf azure-cli-repos-1.0.tar.xz azure-cli-repos-1.0
#
Source:         %{name}-%{version}.tar.xz
Provides:       azure-cli-repos
BuildArch:      noarch

%description
Azure CLI package repository files for yum and dnf along with gpg public keys

%prep
%autosetup

%build

%install
install -d -m 755 %{buildroot}/etc/pki/rpm-gpg
install -m 644 RPM-GPG-* %{buildroot}/etc/pki/rpm-gpg

install -d -m 755 %{buildroot}/etc/yum.repos.d
install -m 644 azure-cli.repo %{buildroot}/etc/yum.repos.d

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*.repo
/etc/pki/rpm-gpg/*

%changelog
* Sun Mar 11 2018 Satoru SATOH <ssato@redhat.com> - 1-0.1
- Initial prototype packaging
