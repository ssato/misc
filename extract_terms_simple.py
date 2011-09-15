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
from itertools import groupby, product

import glob
import logging
import nltk
import optparse
import os
import os.path
import pprint
import re
import subprocess
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


def makeText(path):
    """
    :param path: Input file path
    :return:  nltk.Text instance
    """
    tokens = nltk.word_tokenize(open(path).read())
    return nltk.Text(tokens)


def tf_idf(paths):
    """
    :param paths: A list of input files
    """
    stopwords = nltk.corpus.stopwords.words('english')
    symbols = ["'", '"', '`', '.', ',', '-', '!', '?', ':', ';', '(', ')', '#']

    is_word = lambda s: re.match(r"[a-z]+[a-zA-Z0-9_-]+", s) and not in stopwords

    tokens = lambda path: nltk.word_tokenize(open(path).read())
    text = lambda path: nltk.Text(t for t in tokens(path) if is_word(t.lower()))

    texts = [text(p) for p in paths]
    terms = set(concat(list(txt) for txt in texts))

    tc = nltk.TextCollection(texts)



def opt_parser():
    defaults = init_defaults()
    distribution_choices = defaults["dists_full"]  # save it.

    defaults.update(init_defaults_by_conffile())

    p = optparse.OptionParser("""%prog COMMAND [OPTION ...] [ARGS]

Commands: i[init], b[uild], d[eploy], u[pdate]

Examples:
  # initialize your yum repos:
  %prog init -s yumserver.local -u foo -m foo@example.com -F "John Doe"

  # build SRPM:
  %prog build packagemaker-0.1-1.src.rpm 

  # build SRPM and deploy RPMs and SRPMs into your yum repos:
  %prog deploy packagemaker-0.1-1.src.rpm
  %prog d --dists rhel-6-x86_64 packagemaker-0.1-1.src.rpm
  """
    )

    for k in ("verbose", "quiet", "debug"):
        if not defaults.get(k, False):
            defaults[k] = False

    p.set_defaults(**defaults)

    p.add_option("-C", "--config", help="Configuration file")

    p.add_option("-s", "--server", help="Server to provide your yum repos.")
    p.add_option("-u", "--user", help="Your username on the server [%default]")
    p.add_option("-m", "--email", help="Your email address or its format string[%default]")
    p.add_option("-F", "--fullname", help="Your full name [%default]")

    p.add_option("", "--dists", help="Comma separated distribution labels including arch. "
        "Options are some of " + distribution_choices + " [%default]")

    p.add_option("-q", "--quiet", action="store_true", help="Quiet mode")
    p.add_option("-v", "--verbose", action="store_true", help="Verbose mode")
    p.add_option("", "--debug", action="store_true", help="Debug mode")

    iog = optparse.OptionGroup(p, "Options for 'init' command")
    iog.add_option('', "--name", help="Name of your yum repo or its format string [%default].")
    iog.add_option("", "--subdir", help="Repository sub dir name [%default]")
    iog.add_option("", "--topdir", help="Repository top dir or its format string [%default]")
    iog.add_option('', "--baseurl", help="Repository base URL or its format string [%default]")
    iog.add_option('', "--signkey", help="GPG key ID if signing RPMs to deploy")
    p.add_option_group(iog)

    return p


def do_command(cmd, repos, srpm=None, wait=WAIT_FOREVER):
    f = getattr(RepoOperations, cmd)
    threads = []

    if srpm is not None:
        is_noarch(srpm)  # make a result cache

    for repo in repos:
        args = srpm is None and (repo, ) or (repo, srpm)

        thread = threading.Thread(target=f, args=args)
        thread.start()

        threads.append(thread)

    time.sleep(5)

    for thread in threads:
        # it will block.
        thread.join(wait)

        # Is there any possibility thread still live?
        if thread.is_alive():
            logging.info("Terminating the thread")

            thread.join()


def main(argv=sys.argv):
    (CMD_INIT, CMD_UPDATE, CMD_BUILD, CMD_DEPLOY) = ("init", "update", "build", "deploy")

    logformat = "%(asctime)s [%(levelname)-4s] myrepo: %(message)s"
    logdatefmt = "%H:%M:%S" # too much? "%a, %d %b %Y %H:%M:%S"

    logging.basicConfig(format=logformat, datefmt=logdatefmt)

    p = opt_parser()
    (options, args) = p.parse_args(argv[1:])

    if options.verbose:
        logging.getLogger().setLevel(logging.INFO)
    elif options.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    elif options.quiet:
        logging.getLogger().setLevel(logging.ERROR)
    else:
        logging.getLogger().setLevel(logging.WARN)

    if not args:
        p.print_usage()
        sys.exit(1)

    a0 = args[0]
    if a0.startswith('i'):
        cmd = CMD_INIT

    elif a0.startswith('u'):
        cmd = CMD_UPDATE

    elif a0.startswith('b'):
        cmd = CMD_BUILD
        assert len(args) >= 2, "'%s' command requires an argument to specify srpm[s]" % cmd

    elif a0.startswith('d'):
        cmd = CMD_DEPLOY
        assert len(args) >= 2, "'%s' command requires an argument to specify srpm[s]" % cmd

    else:
        logging.error(" Unknown command '%s'" % a0)
        sys.exit(1)

    if options.config:
        params = init_defaults()
        params.update(init_defaults_by_conffile(options.config))

        p.set_defaults(**params)

        # re-parse to overwrite configurations with given options.
        (options, args) = p.parse_args()

    config = copy.copy(options.__dict__)

    # Kept for DEBUG:
    #pprint.pprint(config)
    #sys.exit()

    dabs = parse_dists_option(config["dists"])  # [(dist, arch, bdist_label)]
    repos = []

    # old way:
    #dists = config["dists"].split(",")
    #for dist, labels in groupby(dists, lambda d: d[:d.rfind("-")]):
    #    archs = [l.split("-")[-1] for l in labels]

    # extended new way:
    for dist, dists in groupby(dabs, lambda d: d[0]):  # d[0]: dist
        dists = list(dists)  # it's a generator and has internal state.

        archs = [d[1] for d in dists]  # d[1]: arch
        bdist_label = [d[2] for d in dists][0]  # d[2]: bdist_label

        repo = Repo(
            config["server"],
            config["user"],
            config["email"],
            config["fullname"],
            dist,
            archs,
            config["name"],
            config["subdir"],
            config["topdir"],
            config["baseurl"],
            config["signkey"],
            bdist_label,
            config["metadata_expire"],
        )

        repos.append(repo)
 
    srpms = args[1:]

    if srpms:
        for srpm in srpms:
            do_command(cmd, repos, srpm)
    else:
        do_command(cmd, repos)

    sys.exit()


if __name__ == '__main__':
    main(sys.argv)

# vim: set sw=4 ts=4 expandtab:
