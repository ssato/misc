# Makefile to download and process files from tepco.

SRC_FORMAT ?= xls
INTERVAL ?= 30

areas = \
tochigi \
ibaraki \
gunma \
chiba \
kanagawa \
tokyo \
saitama \
yamanashi \
$(NULL)

## This data (xls) is different from others.
<<<<<<< HEAD
## (the first cell starts from 'D:0')
=======
## 
>>>>>>> 70380a2ee8c5fd73958817c109ec406cf3bfa309
#areas += numazu


pdf_url_base = http://www.tepco.co.jp/images

SOURCES = $(addsuffix .$(SRC_FORMAT),$(areas))
objs = $(SOURCES:.$(SRC_FORMAT)=.csv)


all: $(objs)


check:
	ping -c1 -w1 www.tepco.co.jp

# FIXME: avoid DOS attack to tepco.
download: check
	cs=""; for f in $(SOURCES); do cs="sleep $(INTERVAL) && curl -O -s -z $$f $(pdf_url_base)/$$f && $$cs"; done; \
		cs="$$cs echo OK"; echo $$cs; eval $$cs


# pdftohtml is not allowed because original pdf file forbids copying texts in it (ouch!).
ifeq ($(SRC_FORMAT),pdf)
%.txt: %.$(SRC_FORMAT)
	pdftotext $< $@

%.csv: %.txt
	python electric_outage_area_list.py $< -o $@
else
%.csv: %.xls
	python electric_outage_area_list.py $< -o $@
endif

clean:
	-rm -f $(SOURCES) $(objs)

.PHONY: clean check download
