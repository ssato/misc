#! /usr/bin/python
"""
    Jinja2 based template renderer.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Compiles and render Jinja2-based template files.

    :copyright: (c) 2012 by Satoru SATOH <ssato@redhat.com>
    :license: BSD-3

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions are met:

   * Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.
   * Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.
   * Neither the name of the author nor the names of its contributors may
     be used to endorse or promote products derived from this software
     without specific prior written permission.
 
 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
 DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


 Requirements: python-jinja2, python-simplejson (python < 2.6) and PyYAML
 References: http://jinja.pocoo.org

"""
from __future__ import print_function

import codecs
import jinja2
import logging
import optparse
import os.path
import sys

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        print(
            "JSON support is disabled as module not found.",
            file=sys.stderr
        )
        json = None

try:
    import yaml
except ImportError:
    print(
        "YAML support is disabled as module not found.",
        file=sys.stderr
    )
    yaml = None


sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
sys.stderr = codecs.getwriter('utf_8')(sys.stderr)


FILETYPES = (FILE_UNKNOWN, FILE_JSON, FILE_YAML) = (0, 1, 2)


def _detect_filetype(filepath):
    """
    >>> FILE_JSON == _detect_filetype("/a/b/c/d.json")
    True
    >>> FILE_YAML == _detect_filetype("/a/b/c/d.yaml")
    True
    >>> FILE_UNKNOWN == _detect_filetype("/a/b/c/d.txt")
    True
    >>> FILE_UNKNOWN == _detect_filetype("/a/b/c/d/e")
    True
    """
    file_and_ext = os.path.splitext(filepath)
    if file_and_ext[1]:
        if file_and_ext[1][1:] in ("json", "jsn"):
            return FILE_JSON

        elif file_and_ext[1][1:] in ("yaml", "yml"):
            return FILE_YAML

    return FILE_UNKNOWN

    
def load_context(filepath):
    """Load context data from given file.

    :param filepath: Context data file path :: str
    """
    filetype = _detect_filetype(filepath)

    if filetype == FILE_UNKNOWN:
        logging.warn("Not supported filetype and skip it: " + filepath)

    elif filetype == FILE_JSON:
        if json is None:
            print(
                "You passed JSON data but JSON support is disabled.",
                file=sys.stderr
            )
            sys.exit(-1)

        logging.info("Loading JSON data from: " + filepath)
        return json.load(open(filepath))

    elif filetype == FILE_YAML:
        if yaml is None:
            print(
                "You passed YAML data but YAML support is disabled.",
                file=sys.stderr
            )
            sys.exit(-1)

        logging.info("Loading YAML data from: " + filepath)
        return yaml.load(open(filepath))

    return {}  # default


def load_contexts(paths):
    """Load context data from given files.

    :param paths: Context data file path list :: [str]
    """
    d = {}
    for path in paths:
        diff = load_context(path)
        d.update(diff)

    return d


def render(filepath, context, template_paths=[]):
    """
    Compile and render template, and returns the result.

    see also: http://jinja.pocoo.org/docs/api/#basics

    :param filepath: (Base) filepath of template file
    :param context: Context dict needed to instantiate templates
    :param template_paths: Template search paths
    """
    topdir = os.path.abspath(os.path.dirname(filepath))
    filename = os.path.basename(filepath)

    paths = [topdir, os.curdir]

    if template_paths:
        paths += template_paths

    paths = list(set(paths))  # uniq
    logging.debug("Template search paths: " + str(paths))

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(paths))

    return env.get_template(filename).render(**context)


def option_parser():
    defaults = dict(
        template_paths=None,
        output=None,
        contexts=[],
        debug=False,
    )

    p = optparse.OptionParser("%prog [OPTION ...] TEMPLATE_FILE")
    p.set_defaults(**defaults)

    p.add_option("-T", "--template-paths",
        help="Coron ':' separated template search paths [.]")
    p.add_option("-o", "--output", help="Output filename [stdout]")
    p.add_option("-C", "--contexts",
        help="Coron ':' separated context data file[s] to instantiate templates"
    )
    p.add_option("-D", "--debug", action="store_true", help="Debug mode")

    return p


def main(argv):
    logging.getLogger().setLevel(logging.INFO)

    p = option_parser()
    (options, args) = p.parse_args(argv[1:])

    if not args:
        p.print_help()
        sys.exit(0)

    if options.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    sep = ":"

    if options.contexts:
        ctx = load_contexts(options.contexts.split(sep))
    else:
        ctx = {}

    if options.template_paths:
        try:
            paths = options.template_paths.split(sep)
        except:
            print(
                "Ignored as invalid form: '%s'" % options.template_paths,
                file=sys.stderr
            )
            paths = []
    else:
        paths = []

    tmpl = args[0]
    result = render(tmpl, ctx, paths)

    if options.output:
        open(options.output, "w").write(result)
    else:
        print(result, file=sys.stdout)


if __name__ == '__main__':
    main(sys.argv)


# vim:sw=4:ts=4:et:
