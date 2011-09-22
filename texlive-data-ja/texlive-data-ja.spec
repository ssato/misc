#%define git     f5dbe3f
%define  savedir  /var/lib/pmaker/preserved
%define  newdir  /var/lib/pmaker/installed


Name:           texlive-data-ja
Version:        0.0.3
Release:        1%{?dist}
Summary:        Latex configuration and data for Japanese tex sources
Group:          Applications/Publishing
License:        MIT
URL:            https://github.com/ssato/misc/tree/master/texlive-data-ja
#Source0:        https://github.com/ssato/misc/tarball/master/%{name}-%{git}.tar.gz
Source0:        https://github.com/ssato/misc/tarball/master/%{name}-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       texlive-east-asian
Requires:       dvipdfmx
Requires:       poppler-data
Requires:       ipa-ex-mincho-fonts, ipa-ex-gothic-fonts


%description
This is a temporal package to provide configuration and some data to fix issues
when generating DVIs/PDFs from tex sources in Japanese.


%package        overrides
Summary:        Some more extra data override files owned by other packages
Group:          Applications/Publishing
Requires:       %{name} = %{version}-%{release}
Requires:       texlive-texmf


%description    overrides
Some more extra data will override and replace other packages'.


%prep
%setup -q


%build
%configure --quiet --enable-silent-rules
make %{?_smp_mflags} V=0


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/var/lib/texlive-data-ja-overrides/saved
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/%{name}-overrides
install -m 755 apply-overrides $RPM_BUILD_ROOT%{_libexecdir}/%{name}-overrides
install -m 755 revert-overrides $RPM_BUILD_ROOT%{_libexecdir}/%{name}-overrides


%clean
rm -rf $RPM_BUILD_ROOT


%post
if [ ! -x /usr/bin/texhash ]; then
    cat /usr/share/texmf/default.ls-R > /usr/share/texmf/ls-R
    cat /var/lib/texmf/default.ls-R  > /var/lib/texmf/ls-R
else
    [ -x /usr/bin/texconfig-sys ] && /usr/bin/texconfig-sys rehash 2> /dev/null
fi
if [ -x /usr/sbin/selinuxenabled ] && /usr/sbin/selinuxenabled; then
    [ -x /sbin/restorecon ] && /sbin/restorecon -R /var/lib/texmf/
fi


%postun
[ -x /usr/bin/texconfig-sys ] && /usr/bin/texconfig-sys rehash 2> /dev/null && \
[ -x /usr/sbin/selinuxenabled ] && /usr/sbin/selinuxenabled && \
[ -x /sbin/restorecon ] && /sbin/restorecon -R /var/lib/texmf/ || :


%post           overrides
if [ $1 = 1 -o $1 = 2 ]; then    # install or update
    %{_libexecdir}/%{name}-overrides/apply-overrides
fi


%preun          overrides
if [ $1 = 0 ]; then    # uninstall (! update)
    %{_libexecdir}/%{name}-overrides/revert-overrides
fi


%files
%defattr(-,root,root,-)
%doc README
%doc README.ja
%{_sysconfdir}/fonts/conf.d/90-texlive-local.conf
%{_sysconfdir}/texmf/dvipdfmx/ipaex.map
%{_datadir}/texmf/web2c/texmf.cnf
%{_datadir}texmf/fonts/truetype/ipaex
%{_bindir}/tex2pdf


%files          overrides
%defattr(-,root,root,-)
%doc README
%doc README.ja
%dir /var/lib/texlive-data-ja-overrides/saved
%{_libexecdir}/%{name}-overrides/*-overrides
/var/lib/texlive-data-ja-overrides/new/usr/share/texmf/web2c/texmf.cnf


%changelog
* Thu Sep 22 2011 Satoru SATOH <ssato@redhat.com> - 0.0.3-1
- Initial (static) packaging.
