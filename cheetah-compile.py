#! /usr/bin/python
#
# cheetah-compile.py - cui tool to compile template.
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

import optparse
import os
import os.path
import sys

from Cheetah.Template import Template

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
    else:
        ## FIXME: It might be better to handle exceptions.
        #try:
        #    return load_fun(path)
        #except Exception, e:
        #    sys.stderr.write("Error during loading %s: (%s): %s\n" % (path, repr(e.__class__), str(e)))
        #    ...
        return load_fun(path)

    return {}


def parse_idata_option(optstr, check_exists=False):
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

        if path:
            if check_exists and not os.path.exists(path):
                raise RuntimeError("Path does not exists: " + path)

            return (fmt, path)
    except:
        pass

    return ()


def compile_template(template, params, is_file=False):
    """
    TODO: Add test case that $template is a filename.

    >>> tmpl_s = "a=$a b=$b"
    >>> params = {'a':1, 'b':'b'}
    >>> 
    >>> assert "a=1 b=b" == compile_template(tmpl_s, params)
    """
    if is_file:
        tmpl = Template(file=template, searchList=params)
    else:
        tmpl = Template(source=template, searchList=params)

    return tmpl.respond()


def main(argv=sys.argv):
    defaults = {
        "output": "",
        "idata": "",
    }

    p = optparse.OptionParser("%prog [OPTION ...] TEMPLATE_FILE")
    p.set_defaults(**defaults)

    p.add_option("-o", "--output", help="Output file")
    p.add_option("", "--idata", 
        help="Data format and path to pass it through in the search list, e.g. pickle:data.pkl, json:../data.json.")

    (opts, args) = p.parse_args()

    if not args:
        p.print_usage()
        sys.exit(1)

    template = args[0]
    params = {}

    output = opts.output and open(opts.output, "w") or sys.stdout

    if opts.idata:
        fmt_and_path = parse_idata_option(opts.idata)

        if fmt_and_path:
            idata = load_idata(*fmt_and_path)
            params = idata
            #import pprint; pprint.pprint(params)

    res = compile_template(template, params, is_file=True)
    print >> output, res

    sys.exit()


if __name__ == '__main__':
    main()


# vim: shiftwidth=4 tabstop=4 expandtab:
