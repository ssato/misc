#
# Bootstrap makefile for trac plugins.
#

ARCH ?= x86_64
TARGET_OSVERSION ?= fedora-17-$(ARCH)

SPECS_LOCATION = https://github.com/ssato/misc/raw/master/trac-macros

# The version of trac provided in $(TARGET_OSVERSION):
TRAC_VERSION = 0.12

MODULES	:= \
trac-footnote-macro \
trac-include-macro \
trac-markdown-macro \
trac-movie-macro \
trac-rssembed-macro \
trac-xslt-macro \
$(NULL)

MODULE_STAMPS = $(addsuffix .stamp,$(MODULES))
MODULE_SPECS = $(addsuffix .spec,$(MODULES))

define make-srpm = 
cd $(@:.stamp=) && python setup.py sdist --formats bztar
test -d $(@:.stamp=)/BUILDROOT || mkdir -p $(@:.stamp=)/BUILDROOT && :
rpmbuild --buildroot $(shell pwd)/$(@:.stamp=)/BUILDROOT \
	--define "_topdir $(shell pwd)/$(@:.stamp=)" \
	--define "_builddir $(shell pwd)/$(@:.stamp=)" \
	--define "_rpmdir $(shell pwd)/$(@:.stamp=)" \
	--define "_srcrpmdir $(shell pwd)/$(@:.stamp=)" \
	--define "_sourcedir $(shell pwd)/$(@:.stamp=)/dist" \
	-bs $<
endef

define set-svnrev-rpmspec =
sed 's,@SVNREV@,$(shell LANG=C svn info $(dir $@) | sed -n 's,^Revision: ,,p'),g' $< > $@.tmp && \
mv $@.tmp $@
endef


all: build

check-env.stamp:
	mock --version >/dev/null
	svn --version --quiet >/dev/null
	git --version >/dev/null
	touch $@

pre-build.stamp: check-env.stamp
	mock --init -r $(TARGET_OSVERSION)
	touch $@


$(MODULE_STAMPS): pre-build.stamp
$(MODULE_SPECS):
	test -d .git || curl --silent -O $(SPECS_LOCATION)/$@


# trac-footnote-macro:
trac-footnote-macro:
	svn co http://trac-hacks.org/svn/footnotemacro/trunk/ $@

trac-footnote-macro/trac-footnote-macro.spec: trac-footnote-macro.spec trac-footnote-macro
	$(set-svnrev-rpmspec)

trac-footnote-macro.stamp: trac-footnote-macro/trac-footnote-macro.spec
	$(make-srpm)
	touch $@


# trac-include-macro:
trac-include-macro:
	svn co http://trac-hacks.org/svn/includemacro/trunk/ $@

trac-include-macro/trac-include-macro.spec: trac-include-macro.spec trac-include-macro
	$(set-svnrev-rpmspec)

trac-include-macro.stamp: trac-include-macro/trac-include-macro.spec
	$(make-srpm)
	touch $@


# trac-markdown-macro:
trac-markdown-macro: trac-markdown-macro.spec
	git clone git://github.com/dwclifton/tracmarkdownmacro.git $@.tmp
	mv $@.tmp/0.11/* $@.tmp/
	mv $@.tmp $@

trac-markdown-macro.stamp: trac-markdown-macro.spec trac-markdown-macro
	$(make-srpm)
	touch $@


# trac-movie-macro:
trac-movie-macro:
	svn co http://trac-hacks.org/svn/moviemacro/trunk/ $@

trac-movie-macro.stamp: trac-movie-macro.spec trac-movie-macro
	$(make-srpm)
	touch $@


# trac-rssembed-macro:
trac-rssembed-macro:
	svn co http://trac-hacks.org/svn/rssembedmacro/0.11/ $@

trac-rssembed-macro.stamp: trac-rssembed-macro.spec trac-rssembed-macro
	$(make-srpm)
	touch $@


# trac-xslt-macro:
trac-xslt-macro: trac-xslt-macro.spec
	svn co http://trac-hacks.org/svn/xsltmacro/0.11/ $@

trac-xslt-macro.stamp: trac-xslt-macro.spec trac-xslt-macro
	$(make-srpm)
	touch $@


build: srpms.stamp

srpms.stamp: $(MODULE_STAMPS)

rpms: srpms.stamp
	for m in $(MODULES); do mock -r $(TARGET_OSVERSION) $$m/*.src.rpm && \
		mv /var/lib/mock/$(TARGET_OSVERSION)/result/*.rpm ./; \
	done

clean:
	-rm -f check-env.stamp pre-build.stamp

.PHONY: build clean rpms
