EXTRA_DIST = texlive-data-ja.spec rpm.mk
EXTRA_DIST += apply-overrides revert-overrides

abs_srcdir  ?= .
include $(abs_srcdir)/rpm.mk


pkgdata0dir = /etc/fonts/conf.d
dist_pkgdata0_DATA = \
etc/fonts/conf.d/90-texlive-local.conf \
$(NULL)

pkgdata1dir = /etc/texmf/dvipdfmx
dist_pkgdata1_DATA = \
etc/texmf/dvipdfmx/ipaex.map \
$(NULL)

pkgdata2dir = /usr/bin
dist_pkgdata2_DATA = \
usr/bin/tex2pdf \
$(NULL)

pkgdata3dir = /var/lib/texlive-data-ja-overrides/new/usr/share/texmf/web2c
dist_pkgdata3_DATA = \
var/lib/texlive-data-ja-overrides/new/usr/share/texmf/web2c/texmf.cnf \
$(NULL)


install-data-hook::
	$(AM_V_at)test -d $(DESTDIR)/usr/share/texmf/fonts/truetype/ipaex || $(MKDIR_P) $(DESTDIR)/usr/share/texmf/fonts/truetype/ipaex
	$(AM_V_at)cd $(DESTDIR)/usr/share/texmf/fonts/truetype/ipaex && $(LN_S) /usr/share/fonts/ipa-ex-gothic/ipaexg.ttf ipaexg.ttf

install-data-hook::
	$(AM_V_at)test -d $(DESTDIR)/usr/share/texmf/fonts/truetype/ipaex || $(MKDIR_P) $(DESTDIR)/usr/share/texmf/fonts/truetype/ipaex
	$(AM_V_at)cd $(DESTDIR)/usr/share/texmf/fonts/truetype/ipaex && $(LN_S) /usr/share/fonts/ipa-ex-mincho/ipaexm.ttf ipaexm.ttf


MKDIR_P ?= mkdir -p
SED ?= sed

# vim: set noexpandtab:
