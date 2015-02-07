#! /usr/bin/python
#
# xlsto.py - Convert Excel files to other formats, e.g. csv, sql db.
#
# Copyright (C) 2008 - 2015 Satoru SATOH <satoru.satoh at gmail.com>
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
# Requirements: python-sqlite3 (python < 2.6), python-xlrd, json or simplejson
#
import cStringIO as StringIO
import codecs
import copy
import csv
import logging
import optparse
import os
import sqlite3
import sys
import xlrd

try:
    import json
except ImportError:
    import simplejson as json


"""xlsto.py

Usage:

  ./xlsto.py [Options ...] DATASPEC_FILE

  (-h or --help option will shows usage)


Data spec:

data spec format is JSON. Here is an example.

[
  {
    "location": "http://example.com/pub/xls/",  # optional
    "filepath": "SampleData.xls",  # file path
    "description": "Sample Data List",
    "sheets": [
      {
        "name": "Sheet1",
        "table_name": "sample_data_list",  # database table name will be used
                                           # in sql db.
        "description": "Sample Data List",
        "keys": [[3,0],[3,1],[3,2],[3,3],"test_key0"],  # cell or string list
                                                        # of col names.
        "marker_idx": 0,   # The index of the col to check whether data exists
                           # in row or not. If omitted, 0 will be used.
        "data_range": [[4,-1],[0,12]]  # data range [[row_bein, row_end],
                                       #             [col_bein, col_end]].
                                       # Indices start with 0 and -1 indicates
                                       # infinite, that is, will be detected
                                       # automatically.
      },
      ...
    ]
  },
  ...
]
"""


def normalize_key(key):
    """Normalize key name to be used as SQL key name.

    >>> normalize_key('Key Name')
    'key_name'
    >>>
    """
    return key.lower().strip().replace(' ', '_')


def rename_if_exists(target, suffix='.bak'):
    """
    If the file $target (file or dir) exists, it will be renamed and backed
    up as 'TARGET.${suffix}'. (The default suffix is '.bak'.)
    """
    if os.path.exists(target):
        os.rename(target, target + suffix)


def load_specs(specfile):
    """Loads given data spec and returns it as an internal representation.
    See the spec example above also.
    """
    return json.load(open(specfile, 'r'))


def load_datasets(specfile, filepath):
    """Loads datasets from Excel workbooks (files) according to each file spec
    in specfile and returns these as dict objects.
    """
    for filespec in load_specs(specfile):
        book = xlrd.open_workbook(filepath)  # throw IndexError, IOError, etc.

        for sheet_idx in range(0, len(filespec['sheets'])):
            sheet = book.sheet_by_index(sheet_idx)
            sheetspec = filespec['sheets'][sheet_idx]
            dataset = copy.copy(sheetspec)

            midx = filespec['sheets'][sheet_idx].get('marker_idx', 0)
            (rows, cols) = sheetspec['data_range']
            if rows[1] == -1:
                rows[1] = sheet.nrows

            # TODO: exceptions handling. (IndexError, etc.)
            keys = [(isinstance(c, list) and sheet.cell_value(*c) or c) for c
                    in sheetspec['keys']]
            values = [sheet.row(rx)[cols[0]:cols[1]+1] for rx in range(*rows)
                      if sheet.row(rx)[midx].value]

            dataset['keynames'] = [normalize_key(k) for k in keys]
            dataset['values'] = values

            yield dataset


# CSV related:
class UnicodeWriter:
    """see the csv example section in the python library reference.
    """
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        self.queue = StringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([isinstance(s, unicode) and s.encode("utf-8") or s
                              for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def csv_process_dataset(outdir, dataset, force):
    """Create db tables and insert datasets into it.
    """
    outfile = dataset['table_name']
    keynames = dataset['keynames']
    values = dataset['values']

    outfile = os.path.sep.join((outdir, outfile + '.csv'))
    logging.info("creating csv file '%s'" % outfile)
    if force:
        rename_if_exists(outfile)

    writer = UnicodeWriter(open(outfile, 'wb'))
    writer.writerow(keynames)

    for xs in values:
        writer.writerow([(x.value and x.value or "") for x in xs])


def csv_create(specfile, filepath, outdir, force):
    """Create the database (create tables and insert datasets into it).
    """
    if not os.path.exists(outdir):
        os.mkdir(outdir, 0755)

    for dataset in load_datasets(specfile, filepath):
        csv_process_dataset(outdir, dataset, force)


# SQLite DB related:
def db_process_dataset(dbfile, dataset):
    """Create db tables and insert datasets into it.
    """
    conn = sqlite3.connect(dbfile)

    table = dataset['table_name']
    keynames = dataset['keynames']
    values = dataset['values']

    keys = ', '.join(keynames).replace('?', '')
    placeholders = ', '.join('?' * len(keynames))

    # 1. create table:
    sql = "create table %s (%s)" % (table, keys)
    logging.info("sql = '%s'" % sql)
    conn.execute(sql)
    conn.commit()

    # 2. insert dataset into the table:
    sql = "insert or replace into %s (%s) values (%s)" % (table, keys,
                                                          placeholders)
    logging.info("sql = '%s'" % sql)

    for xs in values:
        vs = [(x.value and x.value or "") for x in xs]
        if vs:
            logging.info("value = '%s'" % vs)
            conn.execute(sql, vs)
    conn.commit()

    conn.close()


def db_create(specfile, filepath, dbfile, force):
    """Create the database (create tables and insert datasets into it).
    """
    logging.info("creating db '%s'" % dbfile)
    if force:
        rename_if_exists(dbfile)
    for dataset in load_datasets(specfile, filepath):
        db_process_dataset(dbfile, dataset)


def opts_parser():
    psr = optparse.OptionParser('%prog [OPTION ...] INPUT_FILE')
    psr.add_option('-s', '--spec',
                   help="specify 'spec' file defines XLS data structure "
                        "[guessed from input file]")
    psr.add_option('-o', '--output', dest='output', default='output',
                   help="specify database file for 'sqlite' output or dir "
                        "for 'csv' output. [default: output.db or output/]")
    psr.add_option('-t', '--output-type', dest='type',
                   help='Specify the output type, csv or sqlite [default].')
    psr.add_option('-f', '--force', dest='force', action='store_true',
                   help='Force overwrite existing file/dir.', default=False)
    psr.add_option('-v', '--verbose', dest='verbose', action='store_true',
                   help='Verbose mode.', default=False)
    return psr


def main():
    parser = opts_parser()
    (options, args) = parser.parse_args()

    if options.verbose:
        logging.basicConfig(level=logging.INFO)

    out = options.output

    if options.type == 'csv':
        create_f = csv_create
    else:
        create_f = db_create
        if not out.endswith('.db'):
            out = out + '.db'

    if len(args) < 1:
        parser.print_help()
        sys.exit(-1)

    filepath = args[0]

    if options.spec:
        specfile = options.spec
    else:
        specfile = filepath[:filepath.rfind('.')] + '.spec'

    if not os.path.exists(specfile):
        print >> sys.stderr, "Spec file '%s' does not exists!" % specfile
        sys.exit(-1)

    if not os.path.exists(filepath):
        print >> sys.stderr, "Input file '%s' does not exists!" % filepath
        sys.exit(-1)

    create_f(specfile, filepath, out, options.force)


if __name__ == '__main__':
    main()

# vim:sw=4:ts=4:expandtab:
