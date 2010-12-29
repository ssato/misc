#! /usr/bin/python
#
# odf2xxx.py - A command line OpenDocument File converter.
#
# Copyright 2007 Satoru SATOH <ss at gnome.gr.jp>
#
# The Contents of this file are made available subject to
# the terms of GNU Lesser General Public License Version 2.1.
#
# This script is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License version 2.1, as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA  02111-1307  USA
# 
#
# [References]
# Python-UNO bridge http://udk.openoffice.org/python/python-bridge.html
# ooextract.py http://udk.openoffice.org/python/samples/ooextract.py
# 
# [NOTE]
# This script requires an running OpenOffice.org instance accessible from
# UNO bridge. And also, this script and the running OOo instance must be
# able to access the file with by the same system path.
#
# You can run OOo before running this script like the following,
#
# $ ooffice -headless -invisible '-accept=socket,host=localhost,port=2002;urp;'
#
# [TODO]
# How to automate starting OOo instance? (Popen, ...)
#

import getopt
import os
import os.path
import sys


# TODO: At least in Fedora 7+, Python Uno module is not installed in
# the default library path.
try:
        import uno
except ImportError:
        sys.path.append('/usr/lib/openoffice.org/program/')
        import uno

import unohelper

from com.sun.star.beans import PropertyValue
from com.sun.star.uno import Exception, RuntimeException
from com.sun.star.io import IOException, XOutputStream


class OutputStream(unohelper.Base, XOutputStream):
        def __init__(self):
                self.closed = 0
        def closeOutput(self):
                self.closed = 1
        def writeBytes(self, seq):
                sys.stdout.write(seq.value)
        def flush(self):
                pass


def initDesktop(uri):
        """Initialize OOo 'Desktop' (com.sun.start.frame.Desktop)
        instance and returns it.
        """
        lctx = uno.getComponentContext()
        lsmgr = lctx.ServiceManager

        resolver = lsmgr.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", lctx)
        ctx = resolver.resolve(uri)
        smgr = ctx.ServiceManager

        return smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)


def convert(desktop, srcUrl, dstUrl, filter):
        """Convert OD? (srcUrl) to XXX (dstUrl) with filter.
        """
        emsg = ""
        try:
                inProps = (PropertyValue("Hidden" , 0 , True, 0),)
                doc = desktop.loadComponentFromURL(srcUrl, "_blank", 0, inProps)
                if not doc:
                        raise UnoException("Couldn't open stream for unknown reason", None)

                outProps = (
                        PropertyValue("FilterName", 0, filter, 0),
                        PropertyValue("Overwrite", 0, True, 0),
                        PropertyValue("OutputStream", 0, OutputStream(), 0)
                )
                doc.storeToURL(dstUrl, outProps)

        except IOException, e:
                print >> sys.stderr, "Error during conversion: " + e.Message
                raise

        except UnoException, e:
                print >> sys.stderr, "Error (%s) during conversion: %s" % \
                        (repr(e.__class__), e.Message)
                raise

        if doc:
                doc.dispose()

        return emsg


def findFilter(srcFileName, dstFileName):
        """Find out a appropriate filter name from FILTERS.

        >>> findFilter('foo.odt', 'foo.pdf')
        'writer_pdf_Export'
        >>> findFilter('foo.odp', 'foo.ppt')
        'MS PowerPoint 97'
        >>> findFilter('foo.txt', 'foo.pdf')
        None
        """
        filters = {
                'odt' : {
                        'pdf' : 'writer_pdf_Export', 'html' : 'HTML (StarWriter)',
                },
                'odp' : {
                        'pdf' : 'impress_pdf_Export', 'ppt' : 'MS PowerPoint 97',
                },
        }

        f = lambda s: os.path.splitext(s)[1][1:]
        (srcExt, dstExt) = (f(srcFileName), f(dstFileName))

        try:
                return filters[srcExt][dstExt]
        except KeyError:
                return None


def warnOOoNotRunning():
        """
        """
        print >> sys.stderr, """
Please verify the followings,

 * OOo is running
 * connection string is correct ('-c' option in help for more info)
 * OOo is allowing the access from UNO bridge

Or just run,

 ooffice -headless -invisible '-accept=socket,host=localhost,port=2002;urp;'
"""

def usage(ecode, short=False):
        """Usage
        """
        print >> sys.stderr, "Usage: %s [OPTION ...] INPUT OUTPUT" % (sys.argv[0],)
        if not short:
                print >> sys.stderr, """
Options:
  -h, --help         Show this help
  -c, --connection   Specifiy connection string
                     [Default: 'socket,host=localhost,port=2002']
"""
        sys.exit(ecode)


def main():
        """Main.
        """
        uri_tmpl = "uno:%s;urp;StarOffice.ComponentContext"
        constr = 'socket,host=localhost,port=2002'

        uri = uri_tmpl % (constr)

        try:
                opts, args = getopt.getopt(sys.argv[1:], "hc:", ["help", "connection="])
                for o, a in opts:
                        if o in ("-h", "--help"):
                                usage(0)
                        if o in ("-c", "--connection"):
                                uri = uri_tmpl % (a,)
        except getopt.GetoptError:
                usage(1)
        
        if len(args) < 2:
                usage(1, True)

        (src, dst) = args[:2]

        filter = findFilter(src, dst)
        if not filter:
                raise "No suitable filter found. Aborting..."
                sys.exit(1)

        cwd = unohelper.systemPathToFileUrl(os.getcwd())
        p2u = lambda path: unohelper.absolutize(cwd, unohelper.systemPathToFileUrl(path))

        try:
                desktop = initDesktop(uri)
                convert(desktop, p2u(src), p2u(dst), filter)

        except com.sun.star.connection.NoConnectException, e:
                print >> sys.stderr, e.Message
                warnOOoNotRunning()
                sys.exit(1)

        except Exception, e:
                print >> sys.stderr, "Error (%s) : %s" % (repr(e.__class__), e.Message)
                sys.exit(1)


if __name__ == '__main__':
        main()
