LIVE_KS ?= rhel-7-live-base.ks
LABEL ?= Experimental_RHEL_7_Live_Image
SUDO ?= sudo

all:

build-live-iso-image: build-live-iso-image.stamp
build-live-iso-image.stamp: $(LIVE_KS)
	$(SUDO) livecd-creator --verbose --config=$< --fslabel="$(LABEL)" --cache=/var/cache/live
	touch $@

.PHONY: build-live-iso-image
