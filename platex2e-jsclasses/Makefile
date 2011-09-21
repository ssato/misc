# package specific variables:
RPMSPEC	= texlive-texmf-ptex-platex-jsclasses.spec
SRC0	= jsclasses.zip
SRC1	= jis-tfm.zip
SRC0URL	= http://oku.edu.mie-u.ac.jp/~okumura/jsclasses/$(SRC0)
SRC1URL	= http://oku.edu.mie-u.ac.jp/~okumura/texfaq/$(SRC1)


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
	$(FETCH) -o $(WORKDIR)/$(SRC0) $(SRC0URL)
	$(FETCH) -o $(WORKDIR)/$(SRC1) $(SRC1URL)
	touch $@

build-rpms: $(RPMSPEC) $(WORKDIR)/$(SRC0).stamp
	$(make-rpms)


.PHONY: build-rpms
