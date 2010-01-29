#! /usr/bin/python
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
import pprint
import sys
import xlwt



class CsvsWorkbook(object):

    default_styles = {
        #'header': xlwt.easyxf('font: name Times New Roman, color-index red, bold on'),
        'header': xlwt.easyxf('font: name Times New Roman, bold on'),
        'main': xlwt.easyxf('font: name Times New Roman'),
    }

    def __init__(self, filename, header_style=False, main_style=False):
        self._filename = filename
        self._workbook = xlwt.Workbook()
        self._sheets = 0
        self.__init_styles(header_style, main_style)

    def __init_styles(self, header_style, main_style):
        if header_style:
            self._header_style = self.__to_style(header_style, True)
        else:
            self._header_style = self.default_styles['header']

        if main_style:
            self._main_style = self.__to_style(main_style)
        else:
            self._main_style = self.default_styles['main']

    def __del__(self):
        self._workbook.save(self._filename)

    def __to_style(self, style_string, isHeader=False):
        try:
            style = xlwt.easyxf(style_string)
            assert isinstance(style, xlwt.Style.XFStyle)
        except:
            logging.warn(" given style '%s' is not valid. Fall backed to the default." % style_string)
            if isHeader:
                ss = self.default_styles['header']
            else:
                ss = self.default_styles['main']
            style = xlwt.easyxf(ss)

        return style

    def save(self):
        self._workbook.save(self._filename)

    def header_style(self):
        return self._header_style

    def main_style(self):
        return self._main_style

    def sheets(self):
        return self._sheets + 1

    def addWorksheetFromCSVFile(self, csv_filename, csv_encoding='utf-8',
            title=False, fieldnames=[], header_style=False, main_style=False):
        if not title:
            title = "Sheet %d" % (self.sheets())

        _conv = lambda x: unicode(x, csv_encoding)

        reader = csv.reader(open(csv_filename))
        cells = [row for row in reader]

        (headers, dataset) = (cells[0],cells)

        worksheet = self._workbook.add_sheet(title)
        self._sheets += 1

        # header fields: given or get from the first line of the csv file.
        if not fieldnames or (fieldnames and len(fieldnames) < len(headers)):
            fieldnames = headers

        for col in range(0, len(fieldnames)):
            logging.info(" col = %d, fieldname = %s" % (col, fieldnames[col]))
            worksheet.write(0, col, _conv(fieldnames[col]), self.header_style())

        # main data
        for row in range(1, len(dataset)):
            for col in range(0, len(dataset[row])):
                logging.info(" row = %d, col = %d, data = %s" % (row, col, dataset[row][col]))
                worksheet.write(row, col, _conv(dataset[row][col]) or "", self.main_style())



## main:
def opts_parser():
    parser = optparse.OptionParser("%prog [OPTION ...] CSVFILE_0 [CSVFILE_1 ...] OUTPUT_XLS")

    cog = optparse.OptionGroup(parser, "Common Options")
    cog.add_option('', '--sheet-names', help='Comma separated worksheet names')
    cog.add_option('-E', '--encoding', help='Character set encoding of the CSV files [utf-8]', default='utf-8')
    cog.add_option('-v', '--verbose', help='Verbose mode', default=False, action="store_true")
    cog.add_option('-q', '--quiet', help='Quiet mode', default=False, action="store_true")
    parser.add_option_group(cog)
        #'main': xlwt.easyxf('font: name Times New Roman'),

    sog = optparse.OptionGroup(parser, "Style Options")
    sog.add_option('', '--header-style', default='font: name Times New Roman, bold on',
        help='Main (content) style. See xlwt\'s document also, https://secure.simplistix.co.uk/svn/xlwt/trunk/README.html. ["%default"]')
    sog.add_option('', '--main-style', default='font: name Times New Roman',
        help='Main (content) style, ex. "font: name IPAPGothic" for Japanese texts ["%default"]')
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

    logging.basicConfig(level=loglevel)

    if len(args) < 2:
        parser.print_help()
        sys.exit(0)

    csvfiles = args[0:-1]
    output = args[-1]

    if options.sheet_names:
        sheet_names = dict(zip(csvfiles, options.sheet_names.split(',')))

    wb = CsvsWorkbook(output, options.header_style, options.main_style)
    for csvf in csvfiles:
        title = sheet_names.get(csvf, os.path.basename(csvf).replace('.csv',''))
        wb.addWorksheetFromCSVFile(csvf, csv_encoding=options.encoding, title=title)

    wb.save()


def test():
    pass


if __name__ == '__main__':
    main()

# vim: set sw=4 ts=4 expandtab:
