# Makefile to download and process files from tepco.

areas = \
tochigi \
ibaraki \
gunma \
chiba \
kanagawa \
tokyo \
saitama \
yamanashi \
numazu \
$(NULL)

pdf_url_base = http://www.tepco.co.jp/images

pdf_SOURCES = $(addsuffix .pdf,$(areas))
txt_SOURCES = $(pdf_SOURCES:.pdf=.txt)
objs = $(pdf_SOURCES:.pdf=.csv)


all: $(objs)

# FIXME: avoid DOS attack to tepco.
download:
	for f in $(pdf_SOURCES); do curl -O -s -z $$f $(pdf_url_base)/$$f && sleep 3; done

$(objs): download

# pdftohtml is not allowed because original pdf file forbids copying texts in it (ouch!).
%.txt: %.pdf
	pdftotext $< $@

%.csv: %.txt
	python outagelist.py $< -o $@

clean:
	-rm -f $(pdf_SOURCES) $(txt_SOURCES) $(objs)

.PHONY: clean download
