PACKAGE = texlive-data-ja

curdir = $(shell pwd)
WORKDIR = $(curdir)/$(PACKAGE)-build

texlive_SOURCE = \
$(curdir)/etc/fonts/conf.d/90-texlive-local.conf \
$(curdir)/usr/share/texmf/web2c/texmf.cnf \
$(curdir)/usr/bin/tex2pdf,mode=0755 \
$(NULL)

RELATIONS = requires:ipa-ex-mincho-fonts,ipa-ex-gothic-fonts,sazanami-mincho-fonts,sazanami-gothic-fonts,dvipdfmx,texlive-east-asian,poppler-data
URL = http://github.com/ssato/misc/texlive-data-ja

PMAKER = pmaker
PMAKER_FLAGS    = -n $(PACKAGE) \
--license MIT \
--url $(URL) \
--workdir $(WORKDIR) \
--destdir $(curdir) \
--upto sbuild \
--ignore-owner \
$(NULL)



all: texlive-data-ja

$(WORKDIR)/files.list:
	test -d $(WORKDIR) || mkdir -p $(WORKDIR)
	for f in $(texlive_SOURCE); do echo $$f >> $@; done

texlive-data-ja: $(WORKDIR)/files.list
	$(PMAKER) $(PMAKER_FLAGS) \
		--group "Applications/Publishing" \
		--summary "Site (ja) local configuraiton for texlive" \
		--relations $(RELATIONS) $<

.PHONY: texlive-data-ja
