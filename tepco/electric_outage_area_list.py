#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# Convert PDF files published by tepco (Tokyo Denryoku) to other formats: csv
# [, html, json in plan].
#
# Copyright (C) 2011 Satoru SATOH <ssato@redhat.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Requirements: python-xlrd
#

from collections import OrderedDict

import codecs
import cStringIO as StringIO
import csv
import logging
import optparse
import os
import sys
import xlrd



KEYNAMES = (PREF_REGION, CITY_REGION, ADDR_REGION, GRP_REGION) = ('pref', 'city', 'addr', 'grp')



def zip4(x1s, x2s, x3s, x4s):
    """
    >>> zip4([0,3],[1,4],[2,5],[2,3])
    [(0, 1, 2, 2), (3, 4, 5, 3)]
    """
    return [(x1,x2,x3,x4) for ((x1,x2),x3),x4 in zip(zip(zip(x1s, x2s), x3s), x4s)]


def parse_pdf_data(infile):
    """Parse input data file and returns dataset.
    """
    global PREF_REGION, CITY_REGION, ADDR_REGION, GRP_REGION

    region = None

    regions = {
        u"都県": PREF_REGION, 
        u"市区郡": CITY_REGION,
        u"大字通称": ADDR_REGION,
        u"グループ": GRP_REGION,
    }

    data = OrderedDict(pref=[], city=[], addr=[], grp=[])

    for l in codecs.open(infile, encoding='utf-8').readlines():
        if region is None:
            for h in regions.keys():
                if l.startswith(h):
                    region = regions.get(h, None)
                    logging.info("region=" + str(region))
                    continue
        else:
            if l == '\n':
                region = None
            else:
                logging.debug("line=" + l.rstrip())
                data[region].append(l.rstrip())

    return zip4(data[PREF_REGION], data[CITY_REGION], data[ADDR_REGION], data[GRP_REGION])


def parse_xls_data(infile):
    """Parse input xls data file and returns dataset.
    """
    book = xlrd.open_workbook(infile)  # FIXME: might throw IndexError, IOError, etc.
    sheet_idx = 0

    sheet = book.sheet_by_index(sheet_idx)
    keys = (u"都県", u"市区郡", u"大字通称", u"グループ")
    midx = 0
    (rows,cols) = [[1, sheet.nrows], [0,3]]

    data = []

    # TODO: exceptions handling. (IndexError, etc.)
    for rx in range(*rows):
        if sheet.row(rx)[midx].value:
            xs = [(x.value and x.value or "") for x in sheet.row(rx)[cols[0]:cols[1]+1]]

            # FIXME: ugly hack
            try:
                xs[-1] = str(int(xs[-1]))
            except:
                xs[-1] = '?'

            data.append(xs)

    return data



class CsvUnicodeWriter:
    """see the csv example section in the python library reference.
    """
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        self.queue = StringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([isinstance(s, unicode) and s.encode("utf-8") or s for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def out_to_csv(data, outfile, keynames=KEYNAMES):
    """Create db tables and insert datasets into it.
    """
    f = open(outfile, 'wb')

    writer = CsvUnicodeWriter(f)
    writer.writerow(keynames)

    for xs in data:
        writer.writerow(xs)

    f.close()


def main():
    p = optparse.OptionParser('%prog [OPTION ...] INPUT_FILE')
    p.add_option('-o', '--output', help='Specify output file name. default is ${input_file_name_wo_ext}.csv')
    p.add_option('-v', '--verbose', dest='verbose', action='store_true',
        help='Verbose mode.', default=False)

    (options, args) = p.parse_args()

    if options.verbose:
        logging.basicConfig(level=logging.INFO)

    if len(args) < 1:
        p.print_help()
        sys.exit(-1)

    infile = args[0]

    infile_ext = os.path.splitext(infile)[1]
    if infile_ext == '.pdf':
        parse_data_file = parse_pdf_data
    elif infile_ext == '.xls':
        parse_data_file = parse_xls_data
    else:
        logging.error(" Unknown input file format!: " + infile_ext[1:])
        sys.exit(1)

    if options.output:
        outfile = options.output
    else:
        outfile = os.path.splitext(infile)[0] + '.csv'

    if not os.path.exists(infile):
        print >> sys.stderr, "Input file '%s' does not exists!" % filepath
        sys.exit(-1)

    data = parse_data_file(infile)
    out_to_csv(data, outfile, keynames=KEYNAMES)


if __name__ == '__main__':
    main()


# vim: set sw=4 ts=4 expandtab:
