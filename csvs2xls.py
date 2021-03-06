#! /usr/bin/python
#
# Generate an Excel (.xls) file from multiple CSV files.
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
# Requirements: python, python-xlwt (http://pypi.python.org/pypi/xlwt/)
#
"""Generate a Excel file from CSV files

CSV file format:

label_0, label_1, label_2, ....   => Headers
value_0, value_1, ...             => Dataset
...
"""


import csv
import logging
import optparse
import os.path
import os
import pprint  # for debug
import sys
import tempfile
import unittest
import xlwt

from functools import reduce as fold, partial as curry



STDIN_FNAME = 'stdin'



def zipWith(f, xs=[], ys=[]):
    """
    >>> zipWith(max, [3, 3, 8, 2], [2, 1, 5, 7])
    [3, 3, 8, 7]
    >>> zipWith(lambda x, y: (x,y), [3, 3, 8, 2], [2, 1, 5, 7])
    [(3, 2), (3, 1), (8, 5), (2, 7)]
    >>> assert zipWith(lambda x, y: (x,y), [3, 3, 8], [2, 1, 5]) == zip([3, 3, 8], [2, 1, 5])
    >>>

    @TODO: Handle cases if len(xs) != len(ys), for example, use zip' instead of zip
    where
        zip' [] ys = [(None, y)| y <- ys]  # it works if f is max but not if f is min
        zip' xs [] = [(x, None)| x <- xs]  # because min(None, y) returns nothing (undef).
        zip' xs ys = zip xs ys
    """
    assert callable(f)
    return [f(x, y) for x, y in zip(xs, ys)]


def max_col_widths(xss):
    """
    @return list of max width needed for columns (:: [Int]). see an example below.

    >>> xss = [['aaa', 'bbb', 'cccccccc', 'dd'], ['aa', 'b', 'ccccc', 'ddddddd'], ['aaaa', 'bbbb', 'c', 'dd']]
    >>> max_col_widths(xss)
    [4, 4, 8, 7]
    """
    yss = [[len(x) for x in xs] for xs in xss]
    return fold(curry(zipWith, max), yss[1:], yss[0])


def max_col_widths_2(xss):
    """
    More straight-forward implementation optimized for matric.

    >>> xss = [['aaa', 'bbb', 'cccccccc', 'dd'], ['aa', 'b', 'ccccc', 'ddddddd'], ['aaaa', 'bbbb', 'c', 'dd']]
    >>> max_col_widths(xss)
    [4, 4, 8, 7]
    """
    yss = [[len(x) for x in xs] for xs in xss]
    return [max((yss[i][j] for i in range(0, len(yss)))) for j in range(0, len(yss[0]))]


def adjust_width(width):
    """@FIXME: Tune factor and threashold values.
    """
    factor0 = 200
    factor1 = 10
    threashold0 = 15

    if width < threashold0:
        width += factor1

    return width * factor0


def mergeable_cells(xss, row_start=0, row_end=-1, col_start=0, col_end=-1):
    """
    @return (cell_value, r1, r2, c1, c2) of merge-able cells.

    >>> mergeable_cells([['a', 'b', 'c'], ['a', 'c', 'b']])
    [('a', 0, 1, 0, 0)]
    >>> mergeable_cells([['a', 'b', 'c'], ['a', 'c', 'b'], ['c', 'a', 'b'], ['d', 'e', 'b']])
    [('a', 0, 1, 0, 0), ('b', 1, 3, 2, 2)]
    >>> mergeable_cells([['a', 'b', 'c'], ['a', 'c', 'b'], ['c', 'a', 'b'], ['d', 'e', 'b']], 1)
    [('b', 1, 3, 2, 2)]
    >>> mergeable_cells([['a', 'b', 'c'], ['a', 'c', 'b'], ['c', 'a', 'b'], ['d', 'e', 'b']], col_end=1)
    [('a', 0, 1, 0, 0)]
    """
    rl = (row_end < 0 and len(xss) or row_end)
    cl = (col_end < 0 and max((len(xss[r]) for r in range(0, rl))) or col_end)
    ret = []

    for c in range(col_start, cl):
        yss = [(xss[r][c], r, c) for r in range(row_start, rl) if len(xss[r]) > c]
        mss = [[yss[0]]]  # Possibly mergeable cells

        for ys in yss[1:]:
            ms_last = mss[-1]

            if ys[0] == ms_last[-1][0]: # If matched (maybe mergeable),
                if len(ms_last) > 1:    # and there are more than one cells pushed already
                    mss[-1][-1] = ys    # then replace the last cell pushed with it,
                else:
                    mss[-1] += [ys]     # or append it.
            else:
                mss += [[ys]]           # Append the next candidate ms if not matched.

        #pprint.pprint(mss)
        # remove non-mergeable cells having only one cell and convert each pair
        # [(val, r1, c1), (val, r2, c2)] to (val, r1, r2, c1, c2).
        mcs = [(ms[0][0],ms[0][1],ms[1][1],ms[0][2],ms[1][2]) for ms in mss if len(ms) > 1]
        ret += mcs

    return ret


class CsvsWorkbook(object):

    default_styles = {
        'header': 'font: name Times New Roman, bold on',
        'main': 'font: name Times New Roman',
        'merged': 'align: wrap yes, vert center, horiz center',
    }

    def __init__(self, filename, header_style=False, main_style=False, merged_style=False):
        self._filename = filename
        self._workbook = xlwt.Workbook()
        self._sheets = 0
        self.__init_styles(header_style, main_style, merged_style)

    def __init_styles(self, header_style, main_style, merged_style):
        for (sn, ss) in (('header', header_style), ('main', main_style), ('merged', merged_style)):
            self.__init_style(sn, ss)

    def __init_style(self, style_name, style):
        if not style:
            style = self.default_styles[style_name]

        setattr(self, "_%s_style" % style_name, self.__to_style(style_name, style))

    def __del__(self):
        self._workbook.save(self._filename)

    def __to_style(self, style_name, style_string):
        try:
            style = xlwt.easyxf(style_string)
            assert isinstance(style, xlwt.Style.XFStyle)
        except:
            logging.warn(" given style '%s'[%s] is not valid. Fall backed to the default." % (style_string, style_name))
            ss = self.default_styles.get(style_name, self.default_styles['main'])
            style = xlwt.easyxf(ss)

        return style

    def save(self):
        self._workbook.save(self._filename)

    def header_style(self):
        return self._header_style

    def main_style(self):
        return self._main_style

    def merged_style(self):
        return self._merged_style

    def sheets(self):
        return self._sheets + 1

    def addWorksheetFromCSVFile(self, csv_filename, csv_encoding='utf-8',
            title=False, fieldnames=[], header_style=False, main_style=False,
            auto_col_width=False,
            vmerge=False, vmerge_col_end=-1, merged_style=False):
        if not title:
            title = "Sheet %d" % (self.sheets())

        _conv = lambda x: unicode(x, csv_encoding)

        if header_style:
            hstyle = self.__to_style('header', header_style)
        else:
            hstyle = self.header_style()

        if main_style:
            mstyle = self.__to_style('main', main_style)
        else:
            mstyle = self.main_style()

        if merged_style:
            mgstyle = self.__to_style('merged', merged_style)
        else:
            mgstyle = self.merged_style()

        if csv_filename == STDIN_FNAME:
            csvf = sys.stdin
        else:
            csvf = open(csv_filename) 
            
        reader = csv.reader(csvf)
        cells = [row for row in reader]
        csvf.close()

        (headers, dataset) = (cells[0],cells)

        worksheet = self._workbook.add_sheet(title)
        self._sheets += 1

        # header fields: given or get from the first line of the csv file.
        if not fieldnames or (fieldnames and len(fieldnames) < len(headers)):
            fieldnames = headers

        for col in range(0, len(fieldnames)):
            logging.info(" col=%d, fieldname=%s" % (col, fieldnames[col]))
            worksheet.write(0, col, _conv(fieldnames[col]), hstyle)

        # @FIXME: Tune factor and threashold values.
        if auto_col_width:
            mcws = max_col_widths(dataset[1:])  # ignore header columns.

            for i in range(0, len(dataset[0])):
                w = adjust_width(mcws[i])
                logging.info(" col[%d].width=%d [%d](adjusted [original])" % (i, w, mcws[i]))
                worksheet.col(i).width = w

        # main data
        rows = len(dataset)

        if vmerge:
            for ms in mergeable_cells(dataset, 1, col_end=vmerge_col_end):
                worksheet.write_merge(ms[1], ms[2], ms[3], ms[4], _conv(ms[0]), mgstyle)

        for row in range(1, rows):
            for col in range(0, len(dataset[row])):
                logging.info(" row=%d, col=%d, data=%s" % (row, col, dataset[row][col]))
                if vmerge:
                    try:
                        worksheet.write(row, col, _conv(dataset[row][col]) or "", mstyle)
                    except:
                        logging.info("The cell (row=%d, col=%d) is a part of merged cells." % (row, col))
                        pass   # skip this cell as it was written as merged cells before.
                else:
                    worksheet.write(row, col, _conv(dataset[row][col]) or "", mstyle)



## main:
def opts_parser():
    parser = optparse.OptionParser("""%prog [OPTION ...] CSVFILE_0 [CSVFILE_1 ...] OUTPUT_XLS

Examples:
  %prog aaa.csv bbb.csv ccc.csv ABC.xls
  %prog - output.xls  # read csv data from stdin
  %prog --main-style 'font: name IPAPGothic' --sheet-names "aaa,bbb" A.csv B.csv AB.xls
""")

    cog = optparse.OptionGroup(parser, "Common Options")
    cog.add_option('', '--sheet-names', help='Comma separated worksheet names')
    cog.add_option('-E', '--encoding', help='Character set encoding of the CSV files [utf-8]', default='utf-8')
    cog.add_option('-v', '--verbose', help='Verbose mode', default=False, action="store_true")
    cog.add_option('-q', '--quiet', help='Quiet mode', default=False, action="store_true")
    cog.add_option('-T', '--test', help='Test mode - running test suites', default=False, action="store_true")
    parser.add_option_group(cog)
        #'main': xlwt.easyxf('font: name Times New Roman'),

    mog = optparse.OptionGroup(parser, "Cell-merging Options")
    mog.add_option('', '--vmerge', default=False, action="store_true", help='Automatically merge cells having same value')
    mog.add_option('', '--vmerge-col-end', default=-1, type="int", help='Specify the idx of the end column to be merged')
    parser.add_option_group(mog)

    sog = optparse.OptionGroup(parser, "Style Options")
    sog.add_option('', '--auto-col-width', default=False, help='Automatically adjust column widths')
    sog.add_option('', '--header-style', default='font: name Times New Roman, bold on',
        help='Main (content) style. See xlwt\'s document also, https://secure.simplistix.co.uk/svn/xlwt/trunk/README.html. ["%default"]')
    sog.add_option('', '--main-style', default='font: name Times New Roman',
        help='Main (content) style, ex. "font: name IPAPGothic" for Japanese texts ["%default"]')
    sog.add_option('', '--merged-style', default='align: wrap yes, vert center',
        help='Merged cells\' style if --vmerge option is used, ex. "vert center, horiz center ["%default"]')
    parser.add_option_group(sog)

    return parser


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

    if options.test:
        test()

    logging.basicConfig(level=loglevel)

    if len(args) < 2:
        parser.print_help()
        sys.exit(0)

    csvfiles = args[0:-1]
    output = args[-1]

    for i in range(0,len(csvfiles)):
        if csvfiles[i] == '-':
            csvfiles[i] = STDIN_FNAME

    if options.sheet_names:
        sheet_names = dict(zip(csvfiles, options.sheet_names.split(',')))

    wb = CsvsWorkbook(output, options.header_style, options.main_style)
    for csvf in csvfiles:
        title = sheet_names.get(csvf, os.path.basename(csvf).replace('.csv',''))
        wb.addWorksheetFromCSVFile(csvf, csv_encoding=options.encoding, title=title,
            main_style=options.main_style, header_style=options.header_style,
            auto_col_width=options.auto_col_width, 
            vmerge=options.vmerge, vmerge_col_end=options.vmerge_col_end,
            merged_style=options.merged_style)

    wb.save()



class TestScript(unittest.TestCase):
    """TODO: Implement this.
    """
    pass



def test():
    import doctest

    doctest.testmod(verbose=True)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestScript)
    unittest.TextTestRunner(verbosity=2).run(suite)

    sys.exit(0)


if __name__ == '__main__':
    main()

# vim: set sw=4 ts=4 expandtab:
