%bcond_with debug
%bcond_without imap
%bcond_without pop
%bcond_without smtp
%bcond_without gnutls
%bcond_without gss
%bcond_without sasl
%bcond_without idn
%bcond_without hcache
%bcond_without tokyocabinet
%bcond_with bdb
%bcond_with qdbm
%bcond_with gdbm
%bcond_without gpgme

Summary: A text mode mail user agent
Name: mutt
Version: 1.5.21
Release: 10sidebar%{?dist}
Epoch: 5
# The entire source code is GPLv2+ except
# pgpewrap.c setenv.c sha1.c wcwidth.c which are Public Domain
License: GPLv2+ and Public Domain
Group: Applications/Internet
Source: ftp://ftp.mutt.org/pub/mutt/devel/mutt-%{version}.tar.gz
Source1: mutt_ldap_query
Patch2: mutt-1.5.13-nodotlock.patch
Patch3: mutt-1.5.18-muttrc.patch
Patch4: mutt-1.5.18-manual.patch
Patch5: mutt-1.5.21-updating.patch
Patch6: mutt-1.5.21-hdrcnt.patch
Patch7: mutt-1.5.21-testcert.patch
Patch8: mutt-1.5.21-cabundle.patch
Patch9: mutt-1.5.21-gpgme-1.2.0.patch
Patch10: mutt-1.5.21-pophash.patch
Patch11: mutt-1.5.21-certscomp.patch
# http://aur.archlinux.org/packages.php?ID=37609
# http://spacehopper.org/mutt/sidebar-5302767aa6aa.gz
Patch100: mutt-sidebar-5302767aa6aa.patch
Url: http://www.mutt.org/
Requires: mailcap urlview
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: ncurses-devel
BuildRequires: gettext
BuildRequires: automake
# required to build documentation
BuildRequires: docbook-style-xsl libxslt lynx

%if %{with hcache}
%{?with_tokyocabinet:BuildRequires: tokyocabinet-devel}
%{?with_bdb:BuildRequires: db4-devel}
%{?with_qdbm:BuildRequires: qdbm-devel}
%{?with_gdbm:BuildRequires: gdbm-devel}
%endif
%if %{with imap} || %{with pop} || %{with smtp}
%{?with_gnutls:BuildRequires: gnutls-devel}
%{?with_sasl:BuildRequires: cyrus-sasl-devel}
%endif
%if %{with imap}
%{?with_gss:BuildRequires: krb5-devel}
%endif
%{?with_idn:BuildRequires: libidn-devel}
%{?with_gpgme:BuildRequires: gpgme-devel}

%description
Mutt is a small but very powerful text-based MIME mail client.  Mutt
is highly configurable, and is well suited to the mail power user with
advanced features like key bindings, keyboard macros, mail threading,
regular expression searches and a powerful pattern matching language
for selecting groups of messages.

%prep
%setup -q
#./prepare -V
# Thou shalt use fcntl, and only fcntl
%patch2 -p1 -b .nodl
%patch3 -p1 -b .muttrc
%patch4 -p1 -b .manual
%patch5 -p1 -b .updating
%patch6 -p1 -b .hdrcnt
%patch7 -p1 -b .testcert
%patch8 -p1 -b .cabundle
%patch9 -p1 -b .gpgme-1.2.0
%patch10 -p1 -b .pophash
%patch11 -p1 -b .certscomp
%patch100 -p1 -b .sidebar

sed -i.gpgerror 's/`$GPGME_CONFIG --libs`/"\0 -lgpg-error"/' configure

install -p -m644 %{SOURCE1} mutt_ldap_query

%define hgreldate \\.(201[0-9])([0-1][0-9])([0-3][0-9])hg
if echo %{release} | grep -E -q '%{hgreldate}'; then
	echo -n 'const char *ReleaseDate = ' > reldate.h
	echo %{release} | sed -r 's/.*%{hgreldate}.*/"\1-\2-\3";/' >> reldate.h
fi

%build
%configure \
		SENDMAIL=%{_sbindir}/sendmail \
		ISPELL=%{_bindir}/hunspell \
%{?with_debug:	--enable-debug}\
%{?with_pop:	--enable-pop}\
%{?with_imap:	--enable-imap} \
%{?with_smtp:	--enable-smtp} \
%if %{with hcache}
		--enable-hcache \
%{!?with_tokyocabinet:	--without-tokyocabinet} \
%{!?with_gdbm:	--without-gdbm} \
%{!?with_qdbm:	--without-qdbm} \
%endif
%if %{with imap} || %{with pop} || %{with smtp}
%{?with_gnutls:	--with-gnutls} \
%{?with_sasl:	--with-sasl} \
%endif
%if %{with imap}
%{?with_gss: 	--with-gss} \
%endif
%{!?with_idn:	--without-idn} \
%{?with_gpgme:	--enable-gpgme} \
		--with-docdir=%{_docdir}/%{name}-%{version}

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# we like GPG here
cat contrib/gpg.rc >> \
	$RPM_BUILD_ROOT%{_sysconfdir}/Muttrc

grep -5 "^color" contrib/sample.muttrc >> \
	$RPM_BUILD_ROOT%{_sysconfdir}/Muttrc

cat >> $RPM_BUILD_ROOT%{_sysconfdir}/Muttrc <<EOF
source %{_sysconfdir}/Muttrc.local
EOF

echo "# Local configuration for Mutt." > $RPM_BUILD_ROOT%{_sysconfdir}/Muttrc.local

# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/{*.dist,mime.types}
rm -f $RPM_BUILD_ROOT%{_bindir}/{flea,muttbug}
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/{flea,muttbug,mutt_dotlock}.1*
rm -f $RPM_BUILD_ROOT%{_mandir}/man5/{mbox,mmdf}.5*

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/Muttrc
%config(noreplace) %{_sysconfdir}/Muttrc.local
%doc COPYRIGHT ChangeLog GPL NEWS README* UPDATING mutt_ldap_query
%doc contrib/*.rc contrib/sample.* contrib/colors.*
%doc doc/manual.txt doc/smime-notes.txt
%{_bindir}/mutt
%{_bindir}/pgpring
%{_bindir}/pgpewrap
%{_bindir}/smime_keys
%{_mandir}/man1/mutt.*
%{_mandir}/man1/smime_keys.*
%{_mandir}/man5/muttrc.*

%changelog
* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5:1.5.21-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 07 2011 Honza Horak <hhorak@redhat.com> - 5:1.5.21-9
- Fixed a segmentation fault while parsing the certificates file
  (rhbz#750929)

* Wed Nov 02 2011 Honza Horak <hhorak@redhat.com> - 5:1.5.21-8
- Removed ca-bundle.crt since it is outdated (rhbz#734379)
- Build with gpgme support by default (rhbz#748337)
- Fixed segmentation fault during messages removal in thread mode
  (rhbz#674271)

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5:1.5.21-7
- Rebuilt for glibc bug#747377

* Wed Jun 29 2011 Honza Horak <hhorak@redhat.com> - 5:1.5.21-6
- Fixed message indexes when skipping fetch response (mutt bug #3288)

* Fri Apr 15 2011 Honza Horak <hhorak@redhat.com> - 5:1.5.21-5
- Fixed hostname verification of x.509 certificates.
  (rhbz#688756, CVE-2011-1429)

* Tue Mar 29 2011 Honza Horak <hhorak@redhat.com> - 5:1.5.21-4
- Fixed segmentation faults during reading message headers (rhbz#676074)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5:1.5.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 5:1.5.21-2
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Miroslav Lichvar <mlichvar@redhat.com> 5:1.5.21-1
- update to 1.5.21
- link with gpg-error when building with gpgme support (#621626)

* Fri Jul 30 2010 Miroslav Lichvar <mlichvar@redhat.com> 5:1.5.20-3.20100718hg1a35f0
- update to hg snapshot 20100718hg1a35f0

* Thu Dec 17 2009 Deji Akingunola <dakingun@gmail.com> - 5:1.5.20-2.20091214hg736b6a.1
- Rebuild for tokyocabinet new release soname bump

* Wed Dec 16 2009 Miroslav Lichvar <mlichvar@redhat.com> 5:1.5.20-2.20091214hg736b6a
- update to hg snapshot 20091214hg736b6a

* Fri Sep 18 2009 Miroslav Lichvar <mlichvar@redhat.com> 5:1.5.20-1.20090827hg605559
- update to post 1.5.20 hg snapshot (#515148)
- use hunspell by default (#510358)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5:1.5.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 09 2009 Miroslav Lichvar <mlichvar@redhat.com> 5:1.5.19-5
- fix certificate verification (CVE-2009-1390)
- add support for gnutls INSECURE_ALGORITHM error code (#499390) 

* Wed Apr 01 2009 Miroslav Lichvar <mlichvar@redhat.com> 5:1.5.19-4
- use PATH_MAX for buffers passed to realpath (#492861)
- unconditionally inode-sort Maildir and MH folders
- restore connection polling callback when closing SASL connection

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5:1.5.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 14 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 5:1.5.19-2
- Rebuild for deps

* Wed Jan 07 2009 Miroslav Lichvar <mlichvar@redhat.com> 5:1.5.19-1
- update to 1.5.19
- switch hcache backend to tokyocabinet
- drop intr patch

* Mon Jul 28 2008 Miroslav Lichvar <mlichvar@redhat.com> 5:1.5.18-4
- rebuild with db4.7 (Robert Scheck) (#455144)

* Wed Jun 25 2008 Miroslav Lichvar <mlichvar@redhat.com> 5:1.5.18-3
- buildrequire aspell (#452133)
- rebuild with new gnutls

* Mon Jun 02 2008 Miroslav Lichvar <mlichvar@redhat.com> 5:1.5.18-2
- allow interrupts when reading, writing or closing sockets (#447887)
- fix possible crash when opening IMAP mailbox

* Mon May 19 2008 Miroslav Lichvar <mlichvar@redhat.com> 5:1.5.18-1
- update to 1.5.18

* Fri Apr 04 2008 Miroslav Lichvar <mlichvar@redhat.com> 5:1.5.17-4
- fix sending long commands when using gnutls (#438275)
- glob tilde in smime_keys (#424311)
- fix awk script in mutt_ldap_query
- force building with libdb
- make enabling/disabling features in spec easier

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5:1.5.17-3
- Autorebuild for GCC 4.3

* Fri Nov 23 2007 Miroslav Lichvar <mlichvar@redhat.com> 5:1.5.17-2
- don't ignore $from in batch send mode (#392861)
- check Maildir for not being NULL when expanding '='-paths
- prevent mailto parsing buffer overflow by ignoring too long header
- use strtok_r() to parse mailto: links, not strtok()
- update UPDATING

* Fri Nov 02 2007 Miroslav Lichvar <mlichvar@redhat.com> 5:1.5.17-1
- update to 1.5.17

* Mon Sep 17 2007 Miroslav Lichvar <mlichvar@redhat.com> 5:1.5.16-4
- fix md5 on big-endian systems

* Tue Aug 28 2007 Miroslav Lichvar <mlichvar@redhat.com> 5:1.5.16-3
- replace md5 implementation
- update license tag

* Wed Jul 11 2007 Miroslav Lichvar <mlichvar@redhat.com> 5:1.5.16-2
- split urlview off, fix requires and description (#226167)

* Mon Jun 11 2007 Miroslav Lichvar <mlichvar@redhat.com> 5:1.5.16-1
- update to 1.5.16

* Mon May 28 2007 Miroslav Lichvar <mlichvar@redhat.com> 5:1.5.14-4
- validate msgid in APOP authentication (CVE-2007-1558)
- fix overflow in gecos field handling (CVE-2007-2683)

* Mon Mar 19 2007 Miroslav Lichvar <mlichvar@redhat.com> 5:1.5.14-3
- fix building

* Mon Mar 19 2007 Miroslav Lichvar <mlichvar@redhat.com> 5:1.5.14-2
- add check_mbox_size configuration variable; if enabled, file size is used
  instead of access time when checking for new mail
- bind delete key to delete-char (#232601)

* Fri Feb 23 2007 Miroslav Lichvar <mlichvar@redhat.com> 5:1.5.14-1
- update to 1.5.14

* Thu Feb 15 2007 Miroslav Lichvar <mlichvar@redhat.com> 5:1.5.13-2.20070212cvs
- update to latest CVS
- enable libidn support (#228158)

* Wed Feb 07 2007 Miroslav Lichvar <mlichvar@redhat.com> 5:1.5.13-1.20070126cvs
- update to 1.5.13, and latest CVS (#168183, #220816)
- spec cleanup

* Wed Dec 06 2006 Miroslav Lichvar <mlichvar@redhat.com> 5:1.4.2.2-5
- use correct fcc folder with IMAP (#217469)
- don't require smtpdaemon, gettext

* Tue Oct 31 2006 Miroslav Lichvar <mlichvar@redhat.com> 5:1.4.2.2-4
- fix POP authentication with latest cyrus-sasl (#212816)

* Tue Oct 24 2006 Miroslav Lichvar <mlichvar@redhat.com> 5:1.4.2.2-3
- fix insecure temp file creation on NFS (#211085, CVE-2006-5297)

* Thu Aug 03 2006 Miroslav Lichvar <mlichvar@redhat.com> 5:1.4.2.2-2
- fix a SASL authentication bug (#199591)

* Mon Jul 17 2006 Miroslav Lichvar <mlichvar@redhat.com> 5:1.4.2.2-1
- update to 1.4.2.2
- fix directories in manual.txt (#162207)
- drop bcc patch (#197408)
- don't package flea

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 5:1.4.2.1-7.1
- rebuild

* Thu Jun 29 2006 Miroslav Lichvar <mlichvar@redhat.com> 5:1.4.2.1-7
- fix a buffer overflow when processing IMAP namespace (#197152, CVE-2006-3242)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5:1.4.2.1-6.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 5:1.4.2.1-6.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov  9 2005 Bill Nottingham <notting@redhat.com> 5:1.4.2.1-6
- rebuild against new ssl libs

* Thu Oct 27 2005 Bill Nottingham <notting@redhat.com> 5:1.4.2.1-5
- add patch from 1.5 branch to fix SASL logging (#157251, #171528)

* Fri Aug 26 2005 Bill Nottingham <notting@redhat.com> 5:1.4.2.1-3
- add patch from 1.5 branch to fix base64 decoding (#166718)

* Mon Mar  7 2005 Bill Nottingham <notting@redhat.com> 5:1.4.2.1-2
- rebuild against new openssl
- fix build with gcc4

* Thu Jan 27 2005 Bill Nottingham <notting@redhat.com> 5:1.4.2.1-1
- update to 1.4.2.1 (#141007, <moritz@barsnick.net>)
- include a /etc/Muttrc.local for site config (#123109)
- add <f2> as a additional help key for terminals that use <f1> internally
  (#139277)

* Wed Sep 15 2004 Nalin Dahyabhai <nalin@redhat.com> 5:1.4.1-10
- expect the server to prompt for additional auth data if we have some to
  send (#129961, upstream #1845)
- use "pop" as the service name instead of "pop-3" when using SASL for POP,
  per rfc1734

* Fri Aug 13 2004 Bill Nottingham <notting@redhat.com> 5:1.4.1-9
- set write_bcc to no by default (since we ship exim)
- build against sasl2 (#126724)

* Mon Jun 28 2004 Bill Nottingham <notting@redhat.com>
- remove autosplat patch (#116769)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  8 2004 Bill Nottingham <notting@redhat.com> 5:1.4.1-7
- link urlview against ncursesw (fixes #125530, indirectly)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Bill Nottingham <notting@redhat.com> 5:1.4.1-5
- add patch to fix menu padding (CAN-2004-0078, #109317)

* Mon Aug 18 2003 Bill Nottingham <notting@redhat.com> 5:1.4.1-4
- rebuild against ncursesw

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 5:1.4.1-3.2
- rebuild

* Mon Jul  7 2003 Bill Nottingham <notting@redhat.com> 5:1.4.1-3
- fix auth to windows KDCs (#98662)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 19 2003 Bill Nottingham <notting@redhat.com> 5:1.4.1-1
- update to 1.4.1, fixes buffer overflow in IMAP code

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jan 20 2003 Bill Nottingham <notting@redhat.com> 5:1.4-9
- add mailcap requires
- change urlview to htmlview as default browser

* Fri Jan 17 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- change urlview to mozilla as default browser

* Tue Jan 7 2003 Nalin Dahyabhai <nalin@redhat.com> 5:1.4-7
- rebuild

* Mon Dec 2 2002 Bill Nottingham <notting@redhat.com> 5:1.4-6
- ship flea

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 5:1.4-5
- remove unpackaged files from the buildroot

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jun 14 2002 Bill Nottingham <notting@redhat.com> 1.4-3
- rebuild against new slang

* Wed May 29 2002 Nalin Dahyabhai <nalin@redhat.com> 1.4-2
- forcibly enable SSL and GSSAPI support

* Wed May 29 2002 Bill Nottingham <notting@redhat.com> 1.4-1
- whoa, 1.4.

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 16 2002 Bill Nottingham <notting@redhat.com>
- autoconf fun

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jan  1 2002 Bill Nottingham <notting@redhat.com>
- update to 1.2.5.1

* Mon Jul 23 2001 Bill Nottingham <notting@redhat.com>
- don't explictly require krb5-libs, etc.; that's what find-requires is for
  (#49780, sort of)

* Sat Jul 21 2001 Tim Powers <timp@redhat.com>
- no more applnk entries, it's cluttering our menus

* Fri Jul 20 2001 Bill Nottingham <notting@redhat.com>
- add slang-devel to buildprereqs (#49531)

* Mon Jun 11 2001 Bill Nottingham <notting@redhat.com>
- add some sample color definitions (#19471)

* Thu May 24 2001 Bill Nottingham <notting@redhat.com>
- fix typo in muttrc.man (#41610)

* Mon May 14 2001 Bill Nottingham <notting@redhat.com>
- use mktemp in muttbug

* Wed May  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- require webclient, not weclient

* Wed May  2 2001 Bill Nottingham <notting@redhat.com>
- build urlview here

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Tue Feb 13 2001 Bill Nottingham <notting@redhat.com>
- change buildprereq to /usr/sbin/sendmail (it's what it should have been
  originally)
- %%langify

* Tue Feb 13 2001 Michael Stefaniuc <mstefani@redhat.com>
- changed buildprereq to smtpdaemon

* Tue Dec 19 2000 Bill Nottingham <notting@redhat.com>
- rebuild; it's just broken
- fix #13196
- buildprereq sendmail

* Fri Dec 01 2000 Bill Nottingham <notting@redhat.com>
- rebuild because of broken fileutils

* Fri Nov 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- include a sample LDAP query script as a doc file

* Mon Nov  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- patch for imap servers that like to volunteer information after AUTHENTICATE

* Thu Aug 24 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment
- force flock() off and fcntl() on in case defaults change

* Tue Aug  8 2000 Nalin Dahyabhai <nalin@redhat.com>
- enable SSL support

* Fri Aug  4 2000 Bill Nottingham <notting@redhat.com>
- add translation to desktop entry

* Fri Jul 28 2000 Bill Nottingham <notting@redhat.com>
- update to 1.2.5i - fixes IMAP bugs

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jul  7 2000 Bill Nottingham <notting@redhat.com>
- 1.2.4i

* Tue Jun 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment (release 3)
- adjust GSSAPI build logic

* Thu Jun 22 2000 Bill Nottingham <notting@redhat.com>
- fix MD5 code

* Wed Jun 21 2000 Bill Nottingham <notting@redhat.com>
- update to 1.2.2i

* Mon Jun 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use aspell

* Sat Jun 10 2000 Bill Nottingham <notting@redhat.com>
- FHS fixes

* Wed May 10 2000 Bill Nottingham <notting@redhat.com>
- add some files

* Tue May  9 2000 Bill Nottingham <notting@redhat.com>
- update to 1.2i

* Tue Apr  4 2000 Bill Nottingham <notting@redhat.com>
- eliminate explicit krb5-configs dependency

* Wed Mar 22 2000 Bill Nottingham <notting@redhat.com>
- auto<foo> is so much fun.

* Wed Mar 01 2000 Nalin Dahyabhai <nalin@redhat.com>
- make kerberos support conditional at compile-time

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- wmconfig -> desktop

* Fri Feb  4 2000 Bill Nottingham <notting@redhat.com>
- keep the makefiles from re-running autoheader, automake, etc.

* Thu Feb  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- add forward-ported sasl patch

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages, other cleanups

* Wed Jan 19 2000 Bill Nottingham <notting@redhat.com>
- 1.0.1

* Mon Jan  3 2000 Bill Nottingham <notting@redhat.com>
- add the sample mime.types to /usr/doc

* Sat Jan  1 2000 Bill Nottingham <notting@redhat.com>
- fix an odd y2k issue on receiving mail from ancient clients

* Fri Oct 21 1999 Bill Nottingham <notting@redhat.com>
- one-point-oh.

* Fri Sep 25 1999 Bill Nottingham <notting@redhat.com>
- add a buffer overflow patch

* Tue Aug 31 1999 Bill Nottingham <notting@redhat.com>
- update to 1.0pre2

* Tue Aug 17 1999 Bill Nottingham <notting@redhat.com>
- update to 0.95.7
- require urlview since the default muttrc uses it

* Mon Jun 21 1999 Bill Nottingham <notting@redhat.com>
- get correct manual path the Right Way(tm)
- make it so it uses default colors even if COLORFGBG isn't set

* Mon Jun 14 1999 Bill Nottingham <notting@redhat.com>
- update to 0.95.6

* Mon Apr 26 1999 Bill Nottingham <notting@redhat.com>
- try and make sure $RPM_OPT_FLAGS gets passed through

* Fri Apr 23 1999 Bill Nottingham <notting@redhat.com>
- update to 0.95.5

* Mon Mar 29 1999 Bill Nottingham <notting@redhat.com>
- sed correct doc path into /etc/Muttrc for viewing manual

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Thu Mar 18 1999 Bill Nottingham <notting@redhat.com>
- strip binary

* Mon Mar  8 1999 Bill Nottingham <notting@redhat.com>
-  update to 0.95.4 - fixes a /tmp race

* Wed Feb 24 1999 Bill Nottingham <notting@redhat.com>
- the RETURN OF WMCONFIG! Aiyeee!

* Fri Feb 12 1999 Bill Nottingham <notting@redhat.com>
- 0.95.3 - fixes mailcap handling

* Mon Jan  4 1999 Bill Nottingham <notting@redhat.com>
- 0.95.1

* Sat Dec 12 1998 Bill Nottingham <notting@redhat.com>
- 0.95

* Fri Jul 31 1998 Bill Nottingham <notting@redhat.com>
- backport some 0.94.2 security fixes
- fix un-setgid
- update to 0.93.2

* Tue Jul 28 1998 Jeff Johnson <jbj@redhat.com>
- security fix
- update to 0.93.1.
- turn off setgid mail.

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 21 1998 Cristian Gafton <gafton@redhat.com>
- updated to 0.91.1

* Fri Apr 10 1998 Cristian Gafton <gafton@redhat.com>
- updated to mutt-0.89.1

* Thu Oct 16 1997 Otto Hammersmith <otto@redhat.com>
- Updated to mutt 0.85.
- added wmconfig entries.
- removed mime.types

* Mon Sep 1 1997 Donnie Barnes <djb@redhat.com>
- Rebuilt to insure all sources were fresh and patches were clean.

* Wed Aug 6 1997 Manoj Kasichainula <manojk@io.com>
- Initial version for 0.81(e)
