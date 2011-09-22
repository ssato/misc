EXTRA_DIST = README.ja
EXTRA_DIST += texlive-data-ja.spec rpm.mk
EXTRA_DIST += apply-overrides revert-overrides

#abs_top_srcdir  ?= $(shell pwd)
include $(abs_top_srcdir)/rpm.mk


pkgdata0dir = /etc/fonts/conf.d
dist_pkgdata0_DATA = $(abs_top_srcdir)/etc/fonts/conf.d/90-texlive-local.conf

pkgdata1dir = /etc/texmf/dvipdfmx
dist_pkgdata1_DATA = $(abs_top_srcdir)/etc/texmf/dvipdfmx/ipaex.map

pkgdata2dir = /usr/bin
dist_pkgdata2_DATA = $(abs_top_srcdir)/usr/bin/tex2pdf

pkgdata3dir = /var/lib/texlive-data-ja-overrides/new/usr/share/texmf/web2c
dist_pkgdata3_DATA = $(abs_top_srcdir)/var/lib/texlive-data-ja-overrides/new/usr/share/texmf/web2c/texmf.cnf


install-data-hook::
	$(AM_V_at)test -d $(DESTDIR)/usr/share/texmf/fonts/truetype/ipaex || $(MKDIR_P) $(DESTDIR)/usr/share/texmf/fonts/truetype/ipaex
	$(AM_V_at)cd $(DESTDIR)/usr/share/texmf/fonts/truetype/ipaex && $(LN_S) /usr/share/fonts/ipa-ex-gothic/ipaexg.ttf ipaexg.ttf

install-data-hook::
	$(AM_V_at)test -d $(DESTDIR)/usr/share/texmf/fonts/truetype/ipaex || $(MKDIR_P) $(DESTDIR)/usr/share/texmf/fonts/truetype/ipaex
	$(AM_V_at)cd $(DESTDIR)/usr/share/texmf/fonts/truetype/ipaex && $(LN_S) /usr/share/fonts/ipa-ex-mincho/ipaexm.ttf ipaexm.ttf


MKDIR_P ?= mkdir -p
SED ?= sed

# vim: set noexpandtab:
