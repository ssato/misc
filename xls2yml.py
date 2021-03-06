#! /usr/bin/python -tt
#
# Convert Excel file to YAML/JSON file[s].
#
# Copyright (C) 2015 Satoru SATOH <ssato@redhat.com>
# License: MIT
#
# Requirements:
#   - python
#   - python-xlrd: http://pypi.python.org/pypi/xlrd/
#
import codecs
import cStringIO
import csv
import itertools
import logging
import optparse
import os.path
import os
import sys
import xlrd

try:
    from collections import OrderedDict as dict
except ImportError:
    pass




class UnicodeWriter(object):
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.

    :see: http://docs.python.org/release/2.5.2/lib/csv-examples.html
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        # self.writer.writerow([s.encode("utf-8") for s in row])
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
    :see: showable_cell_value in examples/xlrdnameAPIdemo.py in
        python-xlrd dist.
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
        v = xlrd.error_text_from_code.get(cell_value,
                                          '<Unknown error code 0x%02x>' %
                                          cell_value)
    else:
        v = cell_value

    return v


def sheet_cell_values_in_the_row_g(sheet, row, datemode=None):
    if datemode is None:
        datemode = sheet.book.datemode

    for y in xrange(0, sheet.ncols):
        ctype = sheet.cell_type(row, y)

        if ctype == xlrd.XL_CELL_EMPTY:
            v = ""
        else:
            v = show(ctype, sheet.cell_value(row, y), datemode)

        yield (y, v)  # row idx, col idx and its value


def sheet_cell_values_g(sheet, row_start):
    datemode = sheet.book.datemode

    for x in xrange(row_start, sheet.nrows):
        for y, v in sheet_cell_values_in_the_row_g(sheet, x, datemode):
            yield (x, y, v)


def fst(tpl_or_list):
    return tpl_or_list[0]


def foreach_sheet_cells_by_row(sheet, row_start=1):
    for k, g in itertools.groupby(sheet_cell_values_g(sheet, row_start), fst):
        yield [t[2] for t in g]


def normalize_key(key_str):
    return key_str.lower().replace(" ", "_")


class DataDumper(object):

    suffix = ".dat"

    def __init__(self, worksheet, name=None, headers=[], outdir=os.curdir):
        self.worksheet = worksheet
        self.name = name is None and self.worksheet.name or name
        self.output = os.path.join(outdir, self.name + self.suffix)

        if headers:
            self.headers = [normalize_key(h) for h in headers]
            self.row_start = 0
        else:
            self.headers = self.get_headers(self.worksheet)
            self.row_start = 1

    def get_headers(self, worksheet):
        return [normalize_key(val) or "-" for idx, val
                in sheet_cell_values_in_the_row_g(worksheet, 0)]

    def open(self, flag="wb"):
        return codecs.open(self.output, flag, encoding='utf-8')

    def foreach_sheet_cells_by_row(self):
        return foreach_sheet_cells_by_row(self.worksheet, self.row_start)

    def dump_impl(self):
        raise NotImplementedError("Children classes must implement this!")

    def dump(self):
        logging.info("Try to dump data in sheet '%s' to '%s'",
                     self.worksheet.name, self.output)
        self.dump_impl()
        logging.info(" Done: %s" % self.output)


class CsvDumper(DataDumper):

    suffix = ".csv"

    def open(self):
        return super(CsvDumper, self).open(flag="wb")

    def dump_impl(self):
        out = self.open()
        writer = UnicodeWriter(out)

        writer.writerow(self.headers)

        for rowdata in self.foreach_sheet_cells_by_row():
            writer.writerow(rowdata)

        out.close()


class JsonDumper(DataDumper):

    suffix = ".json"

    def dump_impl(self):
        data = [dict(zip(self.headers, rowdata)) for rowdata
                in self.foreach_sheet_cells_by_row()]
        json.dump(data, self.open(), ensure_ascii=False, indent=2)


DUMPERS = dict(csv=CsvDumper,  # default
               json=JsonDumper)


def xls_to(xls_file, dumper, outdir, names=[], headers=[], dumper_map=DUMPERS):
    book = xlrd.open_workbook(xls_file)

    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    for n in range(0, book.nsheets):
        sheet = book.sheet_by_index(n)

        if names and len(names) > n:
            name = names[n]
        else:
            name = sheet.name

        dmpr = dumper_map[dumper](sheet, name, headers, outdir)
        dmpr.dump()


def opts_parser(dumper_map=DUMPERS):
    p = optparse.OptionParser("""%prog [OPTION ...] XLS_FILE

Examples:
  %prog ABC.xls --outdir /tmp/outputs
  %prog ABC.xls --names=aaa,bbb,ccc
""")

    dumper_choices = dumper_map.keys()

    defaults = {
        "names": "",
        "headers": "",
        "dumper": "csv",
        "outdir": os.curdir,
        "verbose": False,
        "quiet": False,
    }
    p.set_defaults(**defaults)

    cog = optparse.OptionGroup(p, "Common Options")
    cog.add_option("", "--dumper", type="choice", choices=dumper_choices,
                   help=("Select dump format from %s [%%default]" %
                         ", ".join(dumper_choices)))
    cog.add_option("", "--names", help="Comma separated filenames")
    cog.add_option("", "--headers",
                   help="Comma separated list of headers [default: cell "
                        "contents in 1st row of input .xls]")
    cog.add_option("-o", "--outdir", help="Specify output dir [%default]")
    cog.add_option("-v", "--verbose", help="Verbose mode", action="store_true")
    cog.add_option("-q", "--quiet", help="Quiet mode", action="store_true")
    p.add_option_group(cog)

    return p


def main(dumper_map=DUMPERS):
    loglevel = logging.WARN

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

    names = options.names and options.names.split(',') or []
    headers = options.headers and options.headers.split(',') or []

    xls_file = args[0]

    xls_to(xls_file, options.dumper, options.outdir, names, headers)


if __name__ == '__main__':
    main()

# vim: set sw=4 ts=4 expandtab:
