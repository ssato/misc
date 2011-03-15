#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# Convert PDF files published by tepco (Tokyo Denryoku) to other formats: csv, html, json.
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
#
# Requirements: json or simplejson, python-cheetah.
#

from collections import OrderedDict

import codecs
import cStringIO as StringIO
import csv
import logging
import optparse
import os
import sys

try:
    import json
except ImportError:
    import simplejson as json



KEYNAMES = (PREF_REGION, CITY_REGION, ADDR_REGION, GRP_REGION) = ('pref', 'city', 'addr', 'grp')



def zip4(x1s, x2s, x3s, x4s):
    """
    >>> zip4([0,3],[1,4],[2,5],[2,3])
    [(0, 1, 2, 2), (3, 4, 5, 3)]
    """
    return [(x1,x2,x3,x4) for ((x1,x2),x3),x4 in zip(zip(zip(x1s, x2s), x3s), x4s)]


def parse_data_file(infile):
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
        parser.print_help()
        sys.exit(-1)

    infile = args[0]

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
