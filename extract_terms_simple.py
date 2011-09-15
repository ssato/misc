#! /usr/bin/python
#
# Extract terms from text by Tf-Idf, MC-Value and FLR algorithm.
#
# Copyright (C) 2011 Satoru SATOH <ssato@redhat.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Requirements: createrepo, ssh, packagemaker (see below)
#
# SEE ALSO: createrepo(8)
# SEE ALSO: https://github.com/ssato/packagemaker
#
from functools import reduce as foldl

import argparse
import logging
import itertools
import math
import nltk
import os
import os.path
import pprint
import re
import sys



def memoize(fn):
    """memoization decorator.
    """
    cache = {}

    def wrapped(*args, **kwargs):
        key = repr(args) + repr(kwargs)
        if not cache.has_key(key):
            cache[key] = fn(*args, **kwargs)
        return cache[key]

    return wrapped


def listplus(list_lhs, foldable_rhs):
    """
    (++) in python.
    """
    return list_lhs + list(foldable_rhs)


def concat(xss):
    """
    >>> concat([[]])
    []
    >>> concat((()))
    []
    >>> concat([[1,2,3],[4,5]])
    [1, 2, 3, 4, 5]
    >>> concat([[1,2,3],[4,5,[6,7]]])
    [1, 2, 3, 4, 5, [6, 7]]
    >>> concat(((1,2,3),(4,5,[6,7])))
    [1, 2, 3, 4, 5, [6, 7]]
    >>> concat(((1,2,3),(4,5,[6,7])))
    [1, 2, 3, 4, 5, [6, 7]]
    >>> concat((i, i*2) for i in range(3))
    [0, 0, 1, 2, 2, 4]
    """
    return foldl(listplus, (xs for xs in xss), [])


@memoize
def make_text(path):
    """Returns nltk.Text instance made from given document.

    :param path: Input file path
    :return:  nltk.Text instance
    """
    stopwords = nltk.corpus.stopwords.words("english")
    symbols = [c for c in "~`!@#$%^&*()_+-=|}{\][\":';?><,./"]

    is_word_ch = lambda w: re.match(r"^[a-z]+[a-z0-9_-]+$", w) 

    # FIXME: Any other ideas?
    is_word = lambda w: len(w) > 2 and is_word_ch(w) and w not in stopwords

    tokens = nltk.word_tokenize(open(path).read())

    return nltk.Text(t for t in tokens if is_word(t.lower()))


def tf_idf(paths):
    """Compute tf_idf for all terms in documents (paths).

    tf_idf (term, doc) = tf(term, doc) * idf(term)

    where tf (term, doc) = occurance(term, doc) / (occurance(term, doc) for all docs)
          idf (term) = D / log (number_of_docs_contains term)
          D = number of all docs

    SEE ALSO: http://ja.wikipedia.org/wiki/Tf-idf

    :param paths: A list of input files
    """
    freqs = dict((path, nltk.FreqDist(make_text(path))) for path in paths)
    terms = list(set(concat(freq.keys() for _, freq in freqs.iteritems())))

    occurs = lambda term, path: freqs[path].get(term, 0)
    sum_occurs = lambda term: sum(occurs(term, path) for path in paths)

    occurs = memoize(occurs)
    sum_occurs = memoize(sum_occurs)

    # /home/ssato/.cache/kbase/DOC-15754.txt
    p2key = lambda path: os.path.basename(path)

    def tf(term):
        soccurs = sum_occurs(term)
        logging.debug(" tf: term=%s, sum_occurs=%d" % (term, soccurs))

        return dict(
            (path, x) for path, x in \
                ((p, float(occurs(term, p)) / float(soccurs)) for p in paths) \
            if x != 0
        )

    def idf(term):
        ndocs = len(paths)
        ndocs_have_term = sum(freqs[path].get(term, False) and 1 or 0 for path in paths)
        logging.debug(" idf: term=%s, ndocs=%d, ndocs_have_term=%d" % (term, ndocs, ndocs_have_term))

        return math.log(ndocs / ndocs_have_term)

    tf = memoize(tf)
    idf = memoize(idf)

    def __tf_idf(term):
        return dict((path, tf(term).get(path, 0) * idf(term)) for path in paths)

    return dict((term, __tf_idf(term)) for term in terms)


def tf_idf_w_nltk(paths):
    """
    FIXME: I still don't understand how to use nltk.TextCollection.tf_idf() and
    something goes wrong.

    :param paths: A list of input files
    """
    texts = dict((path, make_text(path)) for path in paths)

    tc = nltk.TextCollection(t for p, t in texts.iteritems())

    tc_idf = dict()
    for path, text in texts.iteritems():
        tc_idf[path] = dict()

        for term in text:
            tc_idf[path][term] = tc.tf_idf(term, text)

    return tc_idf


def main(argv=sys.argv):
    defaults = dict(
        debug = False,
        outdir = os.path.join(os.getcwd(), "results"),
    )

    p = argparse.ArgumentParser(prog=argv[0])
    p.set_defaults(**defaults)

    p.add_argument("-D", "--debug", action="store_true", help="Debug mode")
    p.add_argument("-p", "--paths", nargs="+", help="Input file path list")
    p.add_argument("-o", "--outdir", help="Output directory [%default]")

    args = p.parse_args(argv[1:])

    if not args.paths:
        p.print_usage()
        sys.exit(1)

    logging.getLogger().setLevel(args.debug and logging.DEBUG or logging.WARN)

    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    result = tf_idf(args.paths)
    outfile = os.path.join(args.outdir, "tf_idf.dat")
    pprint.pprint(result, open(outfile, "w"))


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4 ts=4 expandtab:
