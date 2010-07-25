#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# extract_terms.py - Extract terms from text with using MeCab.
#
# Copyright 2008 Satoru SATOH <ssato@redhat.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# References:
#
# * MeCab (http://mecab.sourceforge.net/) 
#   Yet Another Part-of-Speech and Morphological Analyzer.
#
# * mword (http://tanashi.s240.xrea.com/mword/)
#   I borrowed basic FLR implementation from it.
#

import operator
import optparse
import re
import sys

try:
    import MeCab
except ImportError:
    print >> sys.stderr, """%s needs MeCab binding for Python.
Install it (e.g. python-mecab if you use Fedora) first.
""" % sys.argv[0]
    sys.exit(1)


id = lambda x: x
ASCII_RE = re.compile('[a-zA-Z0-9]+')


def is_noun(node):
    return node.feature.startswith('\xe5\x90\x8d\xe8\xa9\x9e')  # '名詞'

def is_ascii(node):
    return ASCII_RE.match(node.surface)

def is_long_enough(node, threshold=1):
    return (len(unicode(node.surface, 'utf-8')) > threshold)

def combinations(ls, acc=[]):
    """
    >>> combinations(['a','b','c','d'])
    ['ab', 'abc', 'abcd', 'bc', 'bcd', 'cd']
    """
    if not ls:
        return acc
    t = ls[0]
    for s in ls[1:]:
        t += s
        acc.append(t)
    return combinations(ls[1:], acc)


def cmp_str_by_len(s0, s1):
    """
    >>> cmp_str_by_len('abc', 'def')
    0
    >>> cmp_str_by_len('abc', 'de')
    1
    >>> cmp_str_by_len('ab', 'def')
    -1
    """
    l0 = len(unicode(s0, 'utf-8'))
    l1 = len(unicode(s1, 'utf-8'))
    if l0 < l1:
        ret = -1
    elif l0 == l1:
        ret = 0
    else:
        ret = 1
    return ret


def node_itr(src_text, opts="", if_filter=lambda *x: True, wrapper=id, **kwargs):
    """Parsed node iterator.
    """
    tagger = MeCab.Tagger(opts)
    node = tagger.parseToNode(src_text)
    while node:
        if if_filter(node):
            yield wrapper(node)
        node = node.next


is_jp_noun = lambda node: is_noun(node) and (not is_ascii(node))

def cn_itr(text):
    """CN (Compound Noun) iterator. 
    """
    cn = []
    for node in node_itr(text):
        if is_jp_noun(node) and is_long_enough(node, 2):
            cn.append(node.surface)
        else:
            if cn:
                yield tuple(cn)
            cn = []
        node = node.next


def flr(text, op=operator.mul):
    """FLR implementation forked from mword (almost same).

      FLR(CN) = freq(CN) * LR(CN)
      
        where freq(CN) = frequency of CN (Compound Noun) in given text
              LR(CN)   = (((FL(N_1) + 1) * (FR(N_1) + 1)) OP ... 
                          ((FL(N_L) + 1) * (FR(N_L) + 1))) ^ (1 / 2L)

                         where OP = operator.mul (*)
    """
    freq = {}  # {CNs: freq0, ...} where CNs = (Noun0, Noun1, ...)

    # lists pairs (left, noun) and (noun, rigth) for term to compute
    # #LN(N) and #RN(N).
    lefts = {}
    rights = {}

    for cn in cn_itr(text):
        freq[cn] = freq.get(cn, 0) + 1
        cnlen = len(cn)
        if cnlen > 1:
            for i in range(cnlen):
                noun = cn[i]
                if i > 0:
                    left = lefts.get(noun, set())
                    left.add(cn[i-1])
                    lefts[noun] = left
                if i < (cnlen - 1):
                    right = rights.get(noun, set())
                    right.add(cn[i+1])
                    rights[noun] = right

    LN = dict([(noun, len(Ls)) for noun, Ls in lefts.items()])
    RN = dict([(noun, len(Rs)) for noun, Rs in rights.items()])

    FLR = {}
    for cn in freq.keys():
        lr = 1
        for noun in cn:
            lr = op(lr, (1 + LN.get(noun, 0)) * (1 + RN.get(noun, 0)))
        lr = pow(lr, 1 / (2.0 * float(len(cn))))
        FLR[cn] = freq[cn] * lr

    return FLR


def mcvalue(text, dummyop=operator.mul):
    """Modified C-Value implementation.

      MC-Value(CN) = length(CN) * (freq(CN) - t(CN)/c(CN))
      
        where length(CN) = CN's length
              freq(CN)   = frequency of CN (Compound Noun) in given text

    """
    freq = {}    # {CN: freq0, ...} where CN = Noun0 + Noun1 + ...
    length = {}  # {CN: len0, ...}

    for cn in cn_itr(text):
        cn = ''.join(cn)  # tuple -> string
        freq[cn] = freq.get(cn, 0) + 1
        length[cn] = length.get(cn, len(unicode(cn, 'utf-8')))

    cn_groups_by_length = {}
    for cn, len_ in length.items():
        cn_groups_by_length[len_] = cn_groups_by_length.get(len_, []) + [cn,]

    cn_groups_list = [[]]  # cn grouped by length; e.g. [[], ['a','b'], ['ab',], [], ['abcd',], ...]
    for i in range(1, max(cn_groups_by_length.keys())+1):
        cn_groups_list.append(cn_groups_by_length.get(i, []))

    mcv = {}
    for cn, len_ in length.items():
        longer_cn_freq_list = [[freq[x] for x in xs] for xs in cn_groups_list[len_:]]
        t = float(sum([sum(xs) for xs in longer_cn_freq_list]))
        c = sum([len(xs) for xs in longer_cn_freq_list])
        mcv[cn] = len_ * (freq[cn] - t/c)

    return mcv


if __name__ == "__main__":
    def main():
        method = flr
        flrop = operator.mul

        usage = "Usage: %prog [OPTION ...] TEXT_FILE\n  where TEXT_FILE = text data file in UTF-8"
        parser = optparse.OptionParser(usage, version='0.1')
        parser.add_option("-m", "--method", dest="method",
            help="Statistical processing method for compound nouns: flr (default) or mcvalue")
        parser.add_option("-f", "--flrop", dest="flrop", help="integral operator for flr: mul (default) or add")
        (options, args) = parser.parse_args()

        if not args:
            parser.error('TEXT_FILE is not given.')

        if options.method and options.method == 'mcvalue':
            method = mcvalue

        if options.flrop and options.flrop == 'add':
            flrop = operator.add

        input = args[0]
        try:
            f = open(input, 'r')
        except IOError:
            print >> sys.stderr, "Could not open input file to process: '%s'" % input
            sys.exit(1)

        result = method(f.read(), flrop)
        for cn, val in result.items():
            print ''.join(cn) + '\t' + str(val)

    main()

# vim: set sw=4 ts=4 et:
