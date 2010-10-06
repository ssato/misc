#! /usr/bin/python
#
# Generate a series of CSV files from an Excel (.xls) file.
#
# Copyright (C) 2010 Satoru SATOH <satoru.satoh at gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#
# Requirements: python, python-xlrd (http://pypi.python.org/pypi/xlrd/)
#

import codecs
import cStringIO
import csv
import logging
import optparse
import os.path
import os
import pprint  # for debug
import sys
import xlrd

from itertools import groupby



# @see http://docs.python.org/release/2.5.2/lib/csv-examples.html
class UnicodeWriter(object):
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        #self.writer.writerow([s.encode("utf-8") for s in row])
        cs = []
        for s in row:
            try:
                c = s.encode("utf-8")
            except:
                c = str(s)
            cs.append(c)
        self.writer.writerow(cs)
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)



def show(cell_type, cell_value, datemode):
    """
    @see showable_cell_value in examples/xlrdnameAPIdemo.py in python-xlrd dist.
    """
    if cell_type == xlrd.XL_CELL_EMPTY:
        v = ''
    elif cell_type == xlrd.XL_CELL_DATE:
        try:
            v = xlrd.xldate_as_tuple(cell_value, datemode)
        except xlrd.XLDateError:
            e1, e2 = sys.exc_info()[:2]
            v = "%s:%s" % (e1.__name__, e2)
    elif cell_type == xlrd.XL_CELL_ERROR:
        v = xlrd.error_text_from_code.get(cell_value, '<Unknown error code 0x%02x>' % cell_value)
    else:
        v = cell_value

    return v


def sheet_cell_values_g(sheet):
    datemode = sheet.book.datemode

    for x in xrange(0, sheet.nrows):
        for y in xrange(0, sheet.ncols):
            ctype = sheet.cell_type(x, y)

            if ctype == xlrd.XL_CELL_EMPTY:
                v = ''
            else:
                v = show(ctype, sheet.cell_value(x, y), datemode)

            yield (x,y,v)  # row idx, col idx and its value


def sheet_cell_rows_g(sheet):
    for k,g in groupby(sheet_cell_values_g(sheet), lambda t: t[0]):
        ret = [t[2] for t in g]
        #logging.info(" vs=%s" % str(ret))
        yield ret


def xls_to_csvs(xls_file, destdir='.', csv_names=[]):
    book = xlrd.open_workbook(xls_file)

    if not os.path.isdir(destdir):
        os.makedirs(destdir)

    for n in range(0, book.nsheets):
        sheet = book.sheet_by_index(n)

        if csv_names and len(csv_names) > n:
            name = csv_names[n]
        else:
            name = sheet.name

        output = os.path.join(destdir, name + '.csv')
        out = open(output, 'wb')
        writer = UnicodeWriter(out)

        logging.info(" Try dumping sheet '%s' to the output: %s" % (name, output))
        for rowdata in sheet_cell_rows_g(sheet):
            writer.writerow(rowdata)

        out.close()
        logging.info(" Done: %s" % output)



## main:
def opts_parser():
    p = optparse.OptionParser("""%prog [OPTION ...] XLS_FILE

Examples:
  %prog ABC.xls -d /tmp/csvs
  %prog ABC.xls --csv-names=aaa,bbb,ccc
""")

    cog = optparse.OptionGroup(p, "Common Options")
    cog.add_option('', '--csv-names', help='Comma separated csv filenames')
    cog.add_option('-d', '--destdir', help='Specify output dir', default='.')
    cog.add_option('-v', '--verbose', help='Verbose mode', default=False, action="store_true")
    cog.add_option('-q', '--quiet', help='Quiet mode', default=False, action="store_true")
    #cog.add_option('-T', '--test', help='Test mode - running test suites', default=False, action="store_true")
    p.add_option_group(cog)

    return p


def main():
    """Entry point.
    """
    loglevel = logging.WARN
    sheet_names = {}

    parser = opts_parser()
    (options, args) = parser.parse_args()

    if options.verbose:
        loglevel = logging.INFO

    if options.quiet:
        loglevel = logging.ERROR

    logging.basicConfig(level=loglevel)

    if len(args) < 1:
        parser.print_help()
        sys.exit(0)

    if options.csv_names:
        csv_names = options.csv_names.split(',')
    else:
        csv_names = []

    xls_file = args[0]

    xls_to_csvs(xls_file, options.destdir, csv_names)



if __name__ == '__main__':
    main()

# vim: set sw=4 ts=4 expandtab:
