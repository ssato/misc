PACKAGE = texlive-data-ja

curdir = $(shell pwd)
WORKDIR = $(curdir)/$(PACKAGE)-build

texlive_SOURCE = \
$(curdir)/etc/fonts/conf.d/90-texlive-local.conf \
$(curdir)/etc/texmf/dvipdfmx/ipaex.map \
$(curdir)/usr/share/texmf/web2c/texmf.cnf \
$(curdir)/usr/share/texmf/fonts/truetype/ipaex/ipaexg.ttf \
$(curdir)/usr/share/texmf/fonts/truetype/ipaex/ipaexm.ttf \
$(curdir)/usr/bin/tex2pdf,mode=0755 \
$(NULL)

RELATIONS = requires:ipa-ex-mincho-fonts,ipa-ex-gothic-fonts,xdvik,dvipdfmx,texlive-east-asian,poppler-data
URL = http://github.com/ssato/misc/texlive-data-ja
PVERSION = 0.0.2


PMAKER = pmaker
PMAKER_FLAGS    = -n $(PACKAGE) \
--license MIT \
--url $(URL) \
--workdir $(WORKDIR) \
--destdir $(curdir) \
--pversion $(PVERSION) \
--upto sbuild \
--ignore-owner \
$(NULL)



all: texlive-data-ja

$(curdir)/usr/share/texmf/fonts/truetype/ipaex/ipaexg.ttf: /usr/share/fonts/ipa-ex-gothic/ipaexg.ttf
	cd $(dirname $@) && ln -s $< ./

$(curdir)/usr/share/texmf/fonts/truetype/ipaex/ipaexm.ttf: /usr/share/fonts/ipa-ex-mincho/ipaexm.ttf
	cd $(dirname $@) && ln -s $< ./

$(WORKDIR)/files.list:
	test -d $(WORKDIR) || mkdir -p $(WORKDIR)
	for f in $(texlive_SOURCE); do echo $$f >> $@; done

texlive-data-ja: $(WORKDIR)/files.list
	$(PMAKER) $(PMAKER_FLAGS) \
		--group "Applications/Publishing" \
		--summary "Site (ja) local configuraiton for texlive" \
		--relations $(RELATIONS) $<

.PHONY: texlive-data-ja
