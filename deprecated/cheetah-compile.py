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
import cPickle as pickle
import getpass
import logging
import optparse
import os
import os.path
import sys
import tempfile
import unittest
import zipfile

from Cheetah.Template import Template


DICT_TYPES = dict
try:
    from collections import OrderedDict as dict
    DICT_TYPES = (DICT_TYPES, dict)

except ImportError:
    pass


#PASSWORD = "sEcr3t"
PASSWORD = "pass"



def zopen(path, mode="r", passwd=PASSWORD):
    original_path = path.rstrip(".zip").strip(os.path.sep)  # relative
    try:
        return zipfile.ZipFile(path).open(original_path, "r", passwd)
    except KeyError:
        original_path = os.path.basename(path.rstrip(".zip"))
        return zipfile.ZipFile(path).open(original_path, "r", passwd)



class DataLoader(object):

    def __init__(self, load_fun, mode="r", zipped=False):
        self.load_fun = load_fun
        self.mode = mode
        self.zipped = zipped

    def __call__(self, path, **kwargs):
        if self.zipped:
            passwd = getpass.getpass()

            return self.load_fun(zopen(path, self.mode, passwd), **kwargs)
        else:
            return self.load_fun(open(path, self.mode), **kwargs)



logging.getLogger().setLevel(logging.WARN)


## Defines idata loaders:
DATA_LOADERS = dict(
    pickle=DataLoader(pickle.load, "rb"),
    pkl=DataLoader(pickle.load, "rb"),
    picklez=DataLoader(pickle.load, "rb", True),
    pklz=DataLoader(pickle.load, "rb", True),
)

try:
    import json
    DATA_LOADERS["json"] = DataLoader(json.load)
    DATA_LOADERS["jsonz"] = DataLoader(json.load, zipped=True)
except ImportError:
    try:
        import simplejson
        DATA_LOADERS["json"] = DataLoader(simplejson.load)
        DATA_LOADERS["jsonz"] = DataLoader(simplejson.load, zipped=True)
    except ImportError:
        logging.info("json module is not found. Disable JSON support...\n")

try:
    import yaml
    DATA_LOADERS["yaml"] = DATA_LOADERS["yml"] = DataLoader(yaml.load)
    DATA_LOADERS["yamlz"] = DATA_LOADERS["ymlz"] = DataLoader(yaml.load, zipped=True)
except ImportError:
    logging.info("yaml module is not found. Disable YAML support...\n")



def ext_from_path(path):
    """
    TODO: More intelligent detection.

    >>> ext_from_path("a.txt")
    'txt'
    >>> ext_from_path("b.txt.zip")
    'zip'
    >>> ext_from_path("a")
    ''
    """
    return os.path.splitext(path)[-1][1:]


def update(lhs, rhs, dict_types=DICT_TYPES):
    """Update lhs with rhs recursively.

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
    >>> 
    >>> d2 = { "a": { "b": [0, 1], "c": [10, 11]} }
    >>> d3 = { "a": { "b": [0, 1, 2, 3]}}
    >>> d = update(d2, d3)
    >>> assert d["a"]["b"] == [0, 1, 2, 3]
    >>> assert d["a"]["c"] == [10, 11]
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


def load_idata(path, format=None, loaders=DATA_LOADERS):
    """Load input data and returns a dict.

    @path     str   Data file path
    @format   str   Data format [option; guessed from the file extension if not passed]
    @loaders  dict  Data loaders for supported formats
    """
    # if it's a zip file, try detecting the original format before zipped.
    if format == "zip":
        original_fmt = os.path.splitext(os.path.splitext(path)[0])[-1][1:]

        if original_fmt:
            format = original_fmt + "z"  # json -> jsonz
        else:
            format = None

    if format is None or not format:
        format = os.path.splitext(path)[-1][1:]
        if not format:
            logging.warn("File path '%s' lacks extension and format is not passed" % path)
            return None

    load_fun = loaders.get(format, None)

    if load_fun is None:
        logging.warn("No loader is available for the requested format: %s\n" % format)
        return None

    logging.info("Loader found for the format=%s, path=%s" % (format, path))

    return load_fun(path)



class Helper_load_idata(unittest.TestCase):

    path_suffix = ".pickle"

    def is_loader_supported(self, format):
        return format in DATA_LOADERS.keys()

    def setUp(self):
        (_fd, self.path) = tempfile.mkstemp(suffix=self.path_suffix)

        self.data = dict(
            a=dict(b=1, c=2, d="aaa"),
            e=[1, 2, 3],
            f="ggg",
        )

    def tearDown(self):
        os.remove(self.path)



class Test_load_idata__pickle(Helper_load_idata):

    def test_load_idata__pickle(self):
        pickle.dump(self.data, open(self.path, "wb"))
        data = load_idata(self.path, "pickle")

        self.assertIsNotNone(data)
        self.assertEquals(data, self.data)

    def test_load_idata__pickle_auto_detect_format(self):
        pickle.dump(self.data, open(self.path, "wb"))
        data = load_idata(self.path)

        self.assertIsNotNone(data)
        self.assertEquals(data, self.data)



class Test_load_idata__json(Helper_load_idata):

    path_suffix = ".json"

    def test_load_idata__json(self):
        if not self.is_loader_supported("json"):
            sys.stderr.write("json is not supported. skip this test")
            return
        else:
            json.dump(self.data, open(self.path, "w"))
            data = load_idata(self.path, "json")

            self.assertIsNotNone(data)
            self.assertEquals(data, self.data)

    def test_load_idata__json_auto_detect_format(self):
        if not self.is_loader_supported("json"):
            sys.stderr.write("json is not supported. skip this test")
            return
        else:
            json.dump(self.data, open(self.path, "w"))
            data = load_idata(self.path)

            self.assertIsNotNone(data)
            self.assertEquals(data, self.data)



class Test_load_idata__yaml(Helper_load_idata):

    path_suffix = ".yaml"

    def test_load_idata__yaml(self):
        if not self.is_loader_supported("yaml"):
            sys.stderr.write("yaml is not supported. skip this test")
            return
        else:
            yaml.dump(self.data, open(self.path, "w"))
            data = load_idata(self.path, "yaml")

            self.assertIsNotNone(data)
            self.assertEquals(data, self.data)

    def test_load_idata__yaml_auto_detect_format(self):
        if not self.is_loader_supported("yaml"):
            sys.stderr.write("yaml is not supported. skip this test")
            return
        else:
            yaml.dump(self.data, open(self.path, "w"))
            data = load_idata(self.path)

            self.assertIsNotNone(data)
            self.assertEquals(data, self.data)



class Helper_load_idata_zipped(Helper_load_idata):

    password = PASSWORD

    def setUp(self):
        super(Helper_load_idata_zipped, self).setUp()
        self.original_path = self.path.rstrip(".zip")
        print >> sys.stderr, "path=%s, original_path=%s" % (self.path, self.original_path)

    def create_zipfile(self):
        zf = zipfile.ZipFile(self.path, "w")
        zf.setpassword(self.password)
        zf.write(self.original_path)
        zf.close()

    def tearDown(self):
        super(Helper_load_idata_zipped, self).tearDown()
        os.remove(self.original_path)



class Test_load_idata__pickle_zip(Helper_load_idata_zipped):

    path_suffix = ".pickle.zip"

    def test_load_idata__pickle(self):
        pickle.dump(self.data, open(self.original_path, "wb"))
        self.create_zipfile()
        data = load_idata(self.path, "picklez")

        self.assertIsNotNone(data)
        self.assertEquals(data, self.data)

    def test_load_idata__pickle_auto_detect_format(self):
        pickle.dump(self.data, open(self.original_path, "wb"))
        self.create_zipfile()
        data = load_idata(self.path, "zip")

        self.assertIsNotNone(data)
        self.assertEquals(data, self.data)



def loads_idata(path_and_maybe_formats, loaders=DATA_LOADERS):
    """Load input data and returns a dict.

    @path_and_maybe_formats  [(str, str | None)]
        A list of (path, format). format may be None or "" (empty str).
    """
    ret = dict()

    for path, format in path_and_maybe_formats:
        updates = load_idata(path, format)

        if updates is None:
            logging.warn("No meaningful data found: " + path)
        else:
            update(ret, updates)

    return ret



class Test_loads_idata(unittest.TestCase):

    def is_loader_supported(self, format):
        return format in DATA_LOADERS.keys()

    def setUp(self):
        dataset = []

        self.data = [
            dict(a=dict(b=1, c=2, d="aaa")),
            dict(e=[1, 2, 3]),
            dict(f="ggg"),
        ]

        self.files = [tempfile.mkstemp(suffix=".pickle")[1]]
        pickle.dump(self.data[0], open(self.files[0], "wb"))

        if self.is_loader_supported("json"):
            self.files.append(tempfile.mkstemp(suffix=".json")[1])
            json.dump(self.data[1], open(self.files[1], "w"))
        else:
            self.files.append(tempfile.mkstemp(suffix=".pickle")[1])
            pickle.dump(self.data[1], open(self.files[1], "wb"))

        if self.is_loader_supported("yaml"):
            self.files.append(tempfile.mkstemp(suffix=".yaml")[1])
            yaml.dump(self.data[2], open(self.files[2], "w"))
        else:
            self.files.append(tempfile.mkstemp(suffix=".pickle")[1])
            pickle.dump(self.data[2], open(self.files[2], "wb"))

    def tearDown(self):
        for path in self.files:
            os.remove(path)

    def test_loads_idata(self):
        data_ref = self.data[0]
        update(data_ref, self.data[1])
        update(data_ref, self.data[2])

        data = loads_idata([(path, ext_from_path(path)) for path in self.files])

        self.assertIsNotNone(data)
        self.assertEquals(data, data_ref)



def parse_idata_option_single(optstr, check_exists=False, sep=":"):
    """

    >>> parse_idata_option_single("/path/to/data.pickle:pickle")
    ('/path/to/data.pickle', 'pickle')
    >>> parse_idata_option_single("data.json")
    ('data.json', 'json')
    >>> parse_idata_option_single("/path/to/data.json.zip:jsonz")
    ('/path/to/data.json.zip', 'jsonz')
    >>> parse_idata_option_single("/path/to/data.yaml.zip")
    ('/path/to/data.yaml.zip', 'yamlz')
    >>> parse_idata_option_single("yaml")
    ()
    """
    if sep in optstr:
        (path, fmt) = optstr.split(":")
    else:
        path = optstr
        fmt = os.path.splitext(path)[-1][1:]  # TODO: More intelligent detection.

        # if it's a zip file, try detecting the original format before zipped.
        if fmt == "zip":
            original_fmt = os.path.splitext(os.path.splitext(path)[0])[-1][1:]

            if original_fmt:
                fmt = original_fmt + "z"  # json -> jsonz
            else:
                fmt = ""

    if path and fmt:
        if check_exists and not os.path.exists(path):
            raise RuntimeError("Not found: " + path)

        return (path, fmt)
    else:
        return ()


def parse_idata_option(optstr, check_exists=False):
    """

    >>> parse_idata_option("/path/to/data.pickle:pickle", False)
    [('/path/to/data.pickle', 'pickle')]
    >>> parse_idata_option("/path/to/data.pickle:pickle,./data2.yaml:yaml,/tmp/data3.json:json", False)
    [('/path/to/data.pickle', 'pickle'), ('./data2.yaml', 'yaml'), ('/tmp/data3.json', 'json')]
    >>> parse_idata_option("data1.json,/tmp/data2.json", False)
    [('data1.json', 'json'), ('/tmp/data2.json', 'json')]
    >>> parse_idata_option("json")
    []
    >>> parse_idata_option("")
    []
    """
    ret = []

    for path_and_format in optstr.split(","):
        p_and_f = parse_idata_option_single(path_and_format, check_exists=check_exists)
        if p_and_f:
            ret.append(p_and_f)

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
        help="Data path [and format] to find params passed when instantiating templates, e.g. data.pkl:pickle, ../data.json.")

    (opts, args) = p.parse_args()

    if not args:
        p.print_usage()
        sys.exit(1)

    template = args[0]
    params = dict()

    output = opts.output and open(opts.output, "w") or sys.stdout

    if opts.idata:
        path_and_formats = parse_idata_option(opts.idata)
        params = loads_idata(path_and_formats)

    res = compile_template(template, params, is_file=True)
    print >> output, res

    sys.exit()


if __name__ == '__main__':
    main()


# vim: shiftwidth=4 tabstop=4 expandtab:
