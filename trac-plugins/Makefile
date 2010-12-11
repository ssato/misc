#
# Bootstrap makefile for trac plugins.
#

ARCH ?= x86_64
TARGET_OSVERSION ?= fedora-14-$(ARCH)

SPECS_LOCATION = https://github.com/ssato/misc/raw/master/trac-plugins

# The version of trac provided in $(TARGET_OSVERSION):
TRAC_VERSION = 0.11

MODULES	:= \
trac-defaultcc-plugin \
trac-ganttcalendar-plugin \
trac-graphviz-plugin \
trac-mscgen-plugin \
trac-reposearch-plugin \
trac-tags-plugin \
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

trac-defaultcc-plugin: trac-defaultcc-plugin.spec
	svn co http://trac-hacks.org/svn/defaultccplugin/trunk/ $@

trac-defaultcc-plugin.stamp: trac-defaultcc-plugin trac-defaultcc-plugin.spec
	$(make-srpm)
	touch $@

trac-ganttcalendar-plugin: trac-ganttcalendar-plugin.spec
	git clone git://recursive-design.com/gantt-calendar.git $@

trac-ganttcalendar-plugin.stamp: trac-ganttcalendar-plugin trac-ganttcalendar-plugin.spec
	$(make-srpm)
	touch $@

trac-graphviz-plugin: trac-graphviz-plugin.spec
	svn co http://trac-hacks.org/svn/graphvizplugin/0.11/ $@

trac-graphviz-plugin.stamp: trac-graphviz-plugin trac-graphviz-plugin.spec
	$(make-srpm)
	touch $@

trac-mscgen-plugin: trac-mscgen-plugin.spec
	svn co http://trac-hacks.org/svn/mscgenplugin/0.11/ $@

trac-mscgen-plugin.stamp: trac-mscgen-plugin trac-mscgen-plugin.spec
	$(make-srpm)
	touch $@

trac-reposearch-plugin: trac-reposearch-plugin.spec
	svn co http://trac-hacks.org/svn/reposearchplugin/0.11/ $@

trac-reposearch-plugin.stamp: trac-reposearch-plugin trac-reposearch-plugin.spec
	$(make-srpm)
	touch $@

trac-tags-plugin: trac-tags-plugin.spec
	svn co http://trac-hacks.org/svn//tagsplugin/tags/0.6/ $@

trac-tags-plugin.stamp: trac-tags-plugin trac-tags-plugin.spec
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
