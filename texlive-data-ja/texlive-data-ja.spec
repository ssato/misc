Name:           texlive-data-ja
Version:        0.0.3
Release:        1%{?dist}
Summary:        Latex configuration and data for Japanese tex sources
Group:          Applications/Publishing
License:        MIT
URL:            https://github.com/ssato/misc/tree/master/texlive-data-ja
Source0:        https://github.com/ssato/misc/tarball/master/%{name}-%{git}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       texlive-east-asian
Requires:       dvipdfmx
Requires:       poppler-data
Requires:       ipa-ex-mincho-fonts, ipa-ex-gothic-fonts


%description
This is a temporal package to provide configuration and some data to fix issues
when generating DVIs/PDFs from tex sources in Japanese.


%prep
%setup -q


%build
%configure --quiet --enable-silent-rules
make %{?_smp_mflags} V=0


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


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


%files
%defattr(-,root,root,-)
%doc README
%doc README.ja
%{_sysconfdir}/fonts/conf.d/90-texlive-local.conf
%{_sysconfdir}/texmf/dvipdfmx/ipaex.map
%{_datadir}/texmf/web2c/texmf.cnf
%{_datadir}texmf/fonts/truetype/ipaex
%{_bindir}/tex2pdf


%changelog
* Thu Sep 22 2011 Satoru SATOH <ssato@redhat.com> - 0.0.3-1
- Initial (static) packaging.
