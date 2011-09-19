EXTRA_DIST = MANIFEST MANIFEST.overrides
EXTRA_DIST += apply-overrides revert-overrides
EXTRA_DIST += texlive-data-ja.spec rpm.mk

abs_srcdir  ?= .
include $(abs_srcdir)/rpm.mk

pkgdata0dir = /etc/fonts/conf.d
dist_pkgdata0_DATA = \
src/etc/fonts/conf.d/90-texlive-local.conf \
$(NULL)

pkgdata1dir = /usr/bin
dist_pkgdata1_DATA = \
src/usr/bin/tex2pdf \
$(NULL)

pkgdata2dir = /var/lib/texlive-data-ja-overrides/new/usr/share/texmf/web2c
dist_pkgdata2_DATA = \
src/var/lib/texlive-data-ja-overrides/new/usr/share/texmf/web2c/texmf.cnf \
$(NULL)



MKDIR_P ?= mkdir -p
SED ?= sed

# vim: set noexpandtab:
