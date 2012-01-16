pkgdata0dir = $(sysconfdir)/fonts/conf.d
dist_pkgdata0_DATA = 90-texlive-local.conf

pkgdata1dir = $(sysconfdir)/texmf/dvipdfmx
dist_pkgdata1_DATA = ipaex.map

dist_bin_SCRIPTS = tex2pdf

if USE_OVERRIDES
pkgdata2dir = $(localstatedir)/lib/$(PACKAGE)-overrides/new/usr/share/texmf/web2c
dist_pkgdata2_DATA = texmf.cnf

pkgdata4dir = $(libexecdir)/$(PACKAGE)-overrides
dist_pkgdata4_SCRIPTS = apply-overrides revert-overrides
endif

install-data-hook::
if USE_OVERRIDES
	$(AM_V_at)$(MKDIR_P) $(DESTDIR)$(localstatedir)/lib/$(PACKAGE)-overrides/saved
endif
	$(AM_V_at)test -d $(DESTDIR)$(datadir)/texmf/fonts/truetype/ipaex || $(MKDIR_P) $(DESTDIR)$(datadir)/texmf/fonts/truetype/ipaex
	$(AM_V_at)cd $(DESTDIR)$(datadir)/texmf/fonts/truetype/ipaex && $(LN_S) /usr/share/fonts/ipa-ex-gothic/ipaexg.ttf ipaexg.ttf
	$(AM_V_at)cd $(DESTDIR)$(datadir)/texmf/fonts/truetype/ipaex && $(LN_S) /usr/share/fonts/ipa-ex-mincho/ipaexm.ttf ipaexm.ttf

