
# package specific variables:
RPMSPEC	= tex-flowfram.spec
SRC0	= flowfram.zip
SRCURL	= http://mirror.ctan.org/macros/latex/contrib/$(SRC0)


# common:
WORKDIR = build
FETCH	= curl --silent --insecure --location

define make-rpms =
test -d  $(WORKDIR)/BUILDROOT || mkdir -p  $(WORKDIR)/BUILDROOT
rpmbuild --buildroot $(PWD)/$(WORKDIR)/BUILDROOT \
    --define "_topdir $(PWD)/$(WORKDIR)" \
    --define "_builddir $(PWD)/$(WORKDIR)" \
    --define "_rpmdir $(PWD)/$(WORKDIR)" \
    --define "_srcrpmdir $(PWD)/$(WORKDIR)" \
    --define "_sourcedir $(PWD)/$(WORKDIR)" \
    -ba  $(RPMSPEC)
endef


all: build-rpms

$(WORKDIR):
	test -d $@ || mkdir -p $@

$(WORKDIR)/$(SRC0).stamp: $(WORKDIR)
	$(FETCH) -o $(WORKDIR)/$(SRC0) $(SRCURL)
	touch $@

build-rpms: $(RPMSPEC) $(WORKDIR)/$(SRC0).stamp
	$(make-rpms)


.PHONY: build-rpms
