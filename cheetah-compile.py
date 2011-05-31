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
import logging
import optparse
import os
import os.path
import sys

from Cheetah.Template import Template


DICT_TYPES = dict
try:
    from collections import OrderedDict as dict
    DICT_TYPES = (DICT_TYPES, dict)

except ImportError:
    pass


## Defines idata loaders:
SUPPORTED_DATA_LOADERS = dict(
    pickle=lambda path, **kwargs: pickle.load(open(path, "rb"), **kwargs)
)

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



logging.getLogger().setLevel(logging.WARN)



def update(lhs, rhs, dict_types=DICT_TYPES):
    """Update lhs with rhs recursively.

    # NOTE: This does not work because isinstance({...}) returns False contrary
    # to my expectation.
    # >>> d = update({"a": 1, "b": 2}, {"b": 3, "c": 4})

    >>> d0 = dict(a=1, b=2); d1 = dict(b=3, c=4)
    >>> d = update(dict(a=1, b=2), dict(b=3, c=4))
    >>> 
    >>> assert len(d.keys()) == len(list(set(d0.keys() + d1.keys())))
    >>> for k, v in d.iteritems():
    ...     assert d[k] == d1.get(k, d0.get(k))
    >>> 
    >>> d = update(dict(a=1, b=dict(c=2, d=4)), dict(b=dict(c=3, e=5), f=6))
    >>> assert isinstance(d["b"], DICT_TYPES)
    >>> assert d["b"]["c"] == 3
    >>> assert d["b"]["d"] == 4
    >>> assert d["b"]["e"] == 5
    """
    assert isinstance(rhs, type(lhs)) or isinstance(lhs, type(rhs)), \
        "Class mismatch: %s vs. %s" % (str(type(lhs)), str(type(rhs)))

    if isinstance(lhs, dict_types):
        for k, v in lhs.iteritems():
            if rhs.has_key(k):
                lhs[k] = isinstance(v, dict_types) and update(v, rhs[k]) or rhs[k]

        for k, v in rhs.iteritems():
            if not lhs.has_key(k):
                lhs[k] = v

        return lhs

    else:
        return rhs is None and lhs or rhs


def load_idata(format_and_paths, loaders=SUPPORTED_DATA_LOADERS):
    """Load input data and returns a dict.

    @format_and_paths  [(str, str)]  A list of (format, path)
    @loaders  dict  Data loaders for supported formats
    """
    ret = dict()

    for format, path in format_and_paths:
        load_fun = loaders.get(format, None)

        if load_fun is None:
            sys.stderr.write("[WARN] No loader is available for the requested format: %s\n" % format)
        else:
            ## FIXME: It might be better to handle exceptions.
            #try:
            #    return load_fun(path)
            #except Exception, e:
            #    sys.stderr.write("Error during loading %s: (%s): %s\n" % (path, repr(e.__class__), str(e)))
            #    ...
            updates = load_fun(path)
            update(ret, updates)

    return ret


def parse_idata_option_single(optstr, check_exists=False, sep=":"):
    """

    >>> parse_idata_option_single("pickle:/path/to/data.pickle")
    ('pickle', '/path/to/data.pickle')
    >>> parse_idata_option_single("data.json")
    ('json', 'data.json')
    >>> parse_idata_option_single("json:")
    ()
    >>> parse_idata_option_single("yaml")
    ()
    """
    if sep in optstr:
        (fmt, path) = optstr.split(":")
    else:
        path = optstr
        fmt = os.path.splitext(path)[-1][1:]

    if fmt and path:
        if check_exists and not os.path.exists(path):
            raise RuntimeError("Not found: " + path)

        return (fmt, path)
    else:
        return ()


def parse_idata_option(optstr, check_exists=False):
    """

    >>> parse_idata_option("pickle:/path/to/data.pickle", False)
    [('pickle', '/path/to/data.pickle')]
    >>> parse_idata_option("pickle:/path/to/data.pickle,yaml:./data2.yaml,json:/tmp/data3.json", False)
    [('pickle', '/path/to/data.pickle'), ('yaml', './data2.yaml'), ('json', '/tmp/data3.json')]
    >>> parse_idata_option("data1.json,/tmp/data2.json", False)
    [('json', 'data1.json'), ('json', '/tmp/data2.json')]
    >>> parse_idata_option("json:")
    []
    >>> parse_idata_option("yaml")
    []
    >>> parse_idata_option("")
    []
    """
    ret = []

    for fmt_and_path in optstr.split(","):
        updates = parse_idata_option_single(fmt_and_path, check_exists=check_exists)
        if updates:
            ret.append(updates)

    return ret


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
    params = dict()

    output = opts.output and open(opts.output, "w") or sys.stdout

    if opts.idata:
        fmt_and_path_list = parse_idata_option(opts.idata)

        if fmt_and_path_list:
            idata = load_idata(fmt_and_path_list)
            params = idata
            #import pprint; pprint.pprint(params)

    res = compile_template(template, params, is_file=True)
    print >> output, res

    sys.exit()


if __name__ == '__main__':
    main()


# vim: shiftwidth=4 tabstop=4 expandtab:
