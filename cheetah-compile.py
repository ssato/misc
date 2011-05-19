#! /usr/bin/python
#
# cheetah-compile.py - enhanced version of 'cheetah' command in python-cheetah.
#
# Copyright (C) 2011 Red Hat, Inc.
# Red Hat Author(s): Satoru SATOH <ssato@redhat.com>
#
# License: same as python-cheetah (see below)
#
# Permission to use, copy, modify, and distribute this software for any purpose
# and without fee is hereby granted, provided that the above copyright notice
# appear in all copies and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the names of the authors
# not be used in advertising or publicity pertaining to distribution of the
# software without specific, written prior permission.
# 
# THE AUTHORS DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
# ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
# AUTHORS BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY
# DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
# Requirements:
#   * python-cheetah
#   * simplejson: if python < 2.6 and you want json support
#   * PyYAML: if you want yaml support
#
# SEE ALSO: python-cheetah: http://cheetahtemplate.org
#

import cPickle as pickle
import optparse
import os
import os.path
import sys

from Cheetah.CheetahWrapper import *

try:
    from functools import partial
except ImportError:
    def partial(func, *args, **kwargs):
        def wrapped(*restargs, **restkwargs):
            _args = list(args)
            _args.extend(restargs)

            _kwargs = dict(kwargs)
            _kwargs.update(restkwargs)

            return func(*_args, **_kwargs)

        return wrapped


## Defines idata loaders:
SUPPORTED_DATA_LOADERS = {
    "pickle": lambda path, **kwargs: pickle.load(open(path, "rb"), **kwargs)
}

try:
    import json
    SUPPORTED_DATA_LOADERS["json"] = lambda path, **kwargs: json.load(open(path), **kwargs)
except ImportError:
    try:
        import simplejson
        SUPPORTED_DATA_LOADERS["json"] = lambda path, **kwargs: simplejson.load(open(path), **kwargs)
    except ImportError:
        sys.stderr.write("[WARN] Could not load json module and it will not be supported.\n")

try:
    import yaml
    SUPPORTED_DATA_LOADERS["yaml"] = lambda path, **kwargs: yaml.load(open(path), **kwargs)
except ImportError:
    sys.stderr.write("[WARN] Could not load yaml module and it will not be supported.\n")



def load_idata(format, path, loaders=SUPPORTED_DATA_LOADERS, **kwargs):
    load_fun = loaders.get(format, None)

    if load_fun is None:
        sys.stderr.write("[WARN] Could not find any loaders for the requested format: %s\n" % format)
        return {}

    try:
        return load_fun(path)
    except Exception, e:
        sys.stderr.write("Error (%s): %s\n" % (repr(e.__class__), str(e)))
        return {}


def parse_idata_option(optstr):
    """

    >>> parse_idata_option("pickle:/path/to/data.pickle")
    ('pickle', '/path/to/data.pickle')
    >>> parse_idata_option("json:")
    ()
    >>> parse_idata_option("yaml")
    ()
    """
    try:
        (fmt, path) = optstr.split(":")

        if path and os.path.exists(path):
            return (fmt, path)
    except:
        pass

    return ()



class ExtCheetahWrapper(CheetahWrapper):

    ##################################################
    ## Modified version of CheetahWrapper.parseOpts:

    def parseOpts(self, args):
        C, D, W = self.chatter, self.debug, self.warn
        self.isCompile = isCompile = self.command[0] == 'c'
        defaultOext = isCompile and ".py" or ".html"
        self.parser = OptionParser()
        pao = self.parser.add_option
        pao("--idir", action="store", dest="idir", default='', help='Input directory (defaults to current directory)')
        pao("--odir", action="store", dest="odir", default="", help='Output directory (defaults to current directory)')
        pao("--iext", action="store", dest="iext", default=".tmpl", help='File input extension (defaults: compile: .tmpl, fill: .tmpl)')
        pao("--oext", action="store", dest="oext", default=defaultOext, help='File output extension (defaults: compile: .py, fill: .html)')
        pao("-R", action="store_true", dest="recurse", default=False, help='Recurse through subdirectories looking for input files')
        pao("--stdout", "-p", action="store_true", dest="stdout", default=False, help='Send output to stdout instead of writing to a file')
        pao("--quiet", action="store_false", dest="verbose", default=True, help='Do not print informational messages to stdout')
        pao("--debug", action="store_true", dest="debug", default=False, help='Print diagnostic/debug information to stderr')
        pao("--env", action="store_true", dest="env", default=False, help='Pass the environment into the search list')
        pao("--pickle", action="store", dest="pickle", default="", help='Unpickle FILE and pass it through in the search list')
        pao("--flat", action="store_true", dest="flat", default=False, help='Do not build destination subdirectories')
        pao("--nobackup", action="store_true", dest="nobackup", default=False, help='Do not make backup files when generating new ones')
        pao("--settings", action="store", dest="compilerSettingsString", default=None, help='String of compiler settings to pass through, e.g. --settings="useNameMapper=False,useFilters=False"')
        pao('--print-settings', action='store_true', dest='print_settings', help='Print out the list of available compiler settings')
        pao("--templateAPIClass", action="store", dest="templateClassName", default=None, help='Name of a subclass of Cheetah.Template.Template to use for compilation, e.g. MyTemplateClass')
        pao("--parallel", action="store", type="int", dest="parallel", default=1, help='Compile/fill templates in parallel, e.g. --parallel=4')
        pao('--shbang', dest='shbang', default='#!/usr/bin/env python', help='Specify the shbang to place at the top of compiled templates, e.g. --shbang="#!/usr/bin/python2.6"')
        
        # Added: 
        pao("--idata", action="store", dest="idata", default="",
            help='Data format and path to pass it through in the search list, e.g. pickle:data.pkl, json:../data.json.')

        opts, files = self.parser.parse_args(args)
        self.opts = opts
        if sys.platform == "win32":
            new_files = []
            for spec in files:
                file_list = glob.glob(spec)
                if file_list:
                    new_files.extend(file_list)
                else:
                    new_files.append(spec)
            files = new_files
        self.pathArgs = files

        D("""\
cheetah compile %s
Options are
%s
Files are %s""", args, pprint.pformat(vars(opts)), files)


        if opts.print_settings:
            print() 
            print('>> Available Cheetah compiler settings:')
            from Cheetah.Compiler import _DEFAULT_COMPILER_SETTINGS
            listing = _DEFAULT_COMPILER_SETTINGS
            listing.sort(key=lambda l: l[0][0].lower())

            for l in listing:
                print('\t%s (default: "%s")\t%s' % l)
            sys.exit(0)

        #cleanup trailing path separators
        seps = [sep for sep in [os.sep, os.altsep] if sep]
        for attr in ['idir', 'odir']:
            for sep in seps:
                path = getattr(opts, attr, None)
                if path and path.endswith(sep):
                    path = path[:-len(sep)]
                    setattr(opts, attr, path)
                    break

        self._fixExts()
        if opts.env:
            self.searchList.insert(0, os.environ)
        if opts.pickle:
            f = open(opts.pickle, 'rb')
            unpickled = pickle.load(f)
            f.close()
            self.searchList.insert(0, unpickled)

        if opts.idata:
            fmt_and_path = parse_idata_option(opts.idata)
            if fmt_and_path:
                idata = load_idata(*fmt_and_path)
                self.searchList.append(idata)


           
if __name__ == '__main__':
    ExtCheetahWrapper().main()

# vim: shiftwidth=4 tabstop=4 expandtab:
