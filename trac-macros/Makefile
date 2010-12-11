#
# Bootstrap makefile for trac plugins.
#

ARCH ?= x86_64
TARGET_OSVERSION ?= fedora-14-$(ARCH)

SPECS_LOCATION = https://github.com/ssato/misc/raw/master/trac-macros

# The version of trac provided in $(TARGET_OSVERSION):
TRAC_VERSION = 0.11

MODULES	:= \
trac-footnote-macro \
trac-include-macro \
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
	-bs $(@:.stamp=).spec
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
	test -d .git || curl -O $(SPECS_LOCATION)/$@

trac-footnote-macro: trac-footnote-macro.spec
	svn co http://trac-hacks.org/svn/footnotemacro/$(TRAC_VERSION)/ $@

trac-footnote-macro.stamp: trac-footnote-macro trac-footnote-macro.spec
	$(make-srpm)
	touch $@

trac-include-macro: trac-include-macro.spec
	svn co http://trac-hacks.org/svn/includemacro/$(TRAC_VERSION)/ $@

trac-include-macro.stamp: trac-include-macro trac-include-macro.spec
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