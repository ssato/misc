#! /usr/bin/python
#
# A simple script to query RHN or RHN Satellite and list updates for given
# 'rpm -qa --qf ...' outputs.
#
# Copyright (C) 2012 Satoru SATOH <ssato@redhat.com>
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.3 or later. This program is distributed in the hope
# that it will be useful, but WITHOUT ANY WARRANTY expressed or implied,
# including the implied warranties of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details. You
# should have received a copy of the GNU General Public License along with this
# program; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# NOTE: This is just an example script to show how to access RHN XML-RPC API in
# python. It is not a product supported by Red Hat and intended for production
# use.
# 
# SEE ALSO: RHN API overview,
#
#   * http://red.ht/OUITaa
#   * https://YOUR_SATELLITE_SERVER/rhn/apidoc/
#
from operator import itemgetter
from itertools import chain, groupby
from logging import DEBUG, INFO

import getpass
import logging
import optparse
import re
import sys
import xmlrpclib
import yum


try:
    chain_from_iterable = chain.from_iterable
except AttributeError:
    # Borrowed from library doc, 9.7.1 Itertools functions:
    def _from_iterable(iterables):
        for it in iterables:
            for element in it:
                yield element

    chain_from_iterable = _from_iterable


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
    return list(chain_from_iterable(xs for xs in xss))


def uniq(iterable):
    """
    Safer version of the above.
    """
    acc = []
    for x in iterable:
        if x not in acc:
            acc.append(x)

    return acc


# RPM NVRE, data NVRE = NVRE {name, version, release, epoch} :
PKEYS = ("name", "version", "release", "epoch")


def shorten_dict_keynames(dic, prefix, keys=[]):
    """Strip extra key prefixes from dict keys.

    >>> d = {"aaa_xxx":"foo", "aaa_y":"Foo Channel"}
    >>> expected = {"xxx":"foo", "y":"Foo Channel"}
    >>> shorten_dict_keynames(d, "aaa_") == expected
    True
    """
    kvs = ((k.replace(prefix, ''), v) for k, v in dic.iteritems())
    return dict(((k, v) for k, v in kvs if k in keys)) if keys else dict(kvs)


def connect(server=None, user=None, password=None):
    if not server:
        server = raw_input('Enter the RHN server to login > ')

    if not user:
        user = raw_input('Enter your RHN login user ID > ')

    if not password:
        password = getpass.getpass('Enter your RHN login password > ')

    srv = xmlrpclib.Server("https://%s/rpc/api" % server)
    sid = srv.auth.login(user, password)  # may throw xmlrpclib.Fault.

    return (srv, sid)


def load_rpms(listfile, keys=PKEYS, sep=','):
    """Return a list of NVRE constructed from given rpm list gotten by:

      rpm -qa --qf "%{n},%{v},%{r},%{e}\n" | sort | uniq

    :return: [NVRE]
    """
    return [
        dict(zip(keys, line.rstrip().split(sep))) for line in
            open(listfile).readlines() if line and not line.startswith("#")
    ]


def normalize_epoch(epoch):
    """Normalize given package's epoch.

    >>> normalize_epoch("(none)")  # rpmdb style
    0
    >>> normalize_epoch(" ")  # yum/rhn style
    0
    >>> normalize_epoch("0")
    0
    >>> normalize_epoch("1")
    1
    """
    if epoch is None:
        return 0

    if isinstance(epoch, str):
        return int(epoch) if re.match(r".*(\d+).*", epoch) else 0
    else:
        assert isinstance(epoch, int), \
            "epoch is not an int object: " + repr(epoch)
        return epoch  # int?


def normalize(nvre):
    """
    >>> p = {"name": "foo", "version": "0.1", "release": 1, "epoch": " "}
    >>> expected = p; expected["epoch"] = 0
    >>> normalize(p) == expected
    True
    """
    nvre["epoch"] = normalize_epoch(nvre["epoch"])
    return nvre


def packages_in_channel_g(server, sid, channel, latest=False):
    """Yield all packages in the channel one by one.

    see: http://red.ht/NI20pk
    """
    if latest:
        rpc = server.channel.software.listLatestPackages
    else:
        rpc = server.channel.software.listAllPackages

    for p in rpc(sid, channel):
        yield normalize(shorten_dict_keynames(p, "package_", PKEYS))


def pcmp(p1, p2):
    """Compare packages by these versions, releases and epoch numbers.

    :param p1, p2: (normalized) NVRE

    TODO: Fallback to rpm.versionCompare if yum is not available?

    # special cases:
    >>> p1 = dict(name="gpg-pubkey", version="00a4d52b", release="4cb9dd70",
    ...           epoch=0,
    ... )
    >>> p2 = dict(name="gpg-pubkey", version="069c8460", release="4d5067bf",
    ...           epoch=0,
    ... )
    >>> pcmp(p1, p1) == 0
    True
    >>> pcmp(p1, p2) < 0
    True

    >>> # compare by releases
    >>> p3 = dict(name="kernel", version="2.6.38.8", release="32", epoch=0)
    >>> p4 = dict(name="kernel", version="2.6.38.8", release="35", epoch=0)
    >>> pcmp(p3, p4) < 0
    True

    >>> # compare by versions and releases
    >>> p5 = dict(name="rsync", version="2.6.8", release="3.1", epoch=0)
    >>> p6 = dict(name="rsync", version="3.0.6", release="4.el5", epoch=0)
    >>> pcmp(p3, p4) < 0
    True

    >>> # compare by epoch numbers
    >>> p7 = dict(name="rsync", version="2.6.8", release="3.1", epoch=2)
    >>> p8 = dict(name="rsync", version="3.0.6", release="4.el5", epoch=0)
    >>> pcmp(p7, p8) > 0
    True
    """
    p2evr = lambda p: (p["epoch"], p["version"], p["release"])
    assert p1["name"] == p2["name"], "Trying to compare different packages!"
    return yum.compareEVR(p2evr(p1), p2evr(p2))


def find_updates_g(ref_ps, ps):
    """Find all updates relevant to given (installed) packages.

    :param ref_ps: all packages including latest updates
    :param ps: (installed) packages to search updates
    """
    def is_newer(p1, p2):
        return pcmp(p1, p2) > 0  # p1 is newer than p2.

    def same_names(p1, p2):
        return p1["name"] == p2["name"]

    for p in ps:
        updates = [c for c in ref_ps if same_names(c, p) and is_newer(c, p)]
        if updates:
            yield uniq(sorted(updates, cmp=pcmp))


def find_latests(ps):
    """Find the latest packages from given packages list, `ps`.
    """
    f = itemgetter("name")
    return [
        normalize(sorted(g, cmp=pcmp)[-1]) for _, g in
            groupby(sorted(ps, key=f), f)
    ]


def opts_parser():
    defaults = dict(
        user=None, passwd=None, server=None, channels=[], latest=False,
        format="%(name)s-%(version)s-%(release)s:%(epoch)s",
        verbose=False,
    )

    p = optparse.OptionParser("%prog [OPTION ...] RPMS_LISTFILE")
    p.set_defaults(**defaults)

    p.add_option("-u", "--user", help="RHN login id")
    p.add_option("-p", "--passwd", help="RHN Login password")
    p.add_option("-s", "--server", help="RHN Server")
    p.add_option("-f", "--format",
        help="specify custom output format (python format string), "
            "e.g. \"%%(name)s %%(version)s\" [name-version-release:epoch]"
    )
    p.add_option("-c", "--channels", action="append",
        help="Software channel label to search the packages."
    )
    p.add_option("-l", "--latest", action="store_true",
        help="Get latest packages info only"
    )
    p.add_option("-v", "--verbose", action="store_true", help="Verbose mode")

    return p


def main():
    p = opts_parser()
    (options, args) = p.parse_args()

    if not args:
        p.print_help()
        sys.exit(0)

    logging.basicConfig(
        format="%(asctime)-15s - %(levelname)s - %(message)s",
        level=(DEBUG if options.verbose else INFO),
    )

    rpmlist = args[0]
    rpms = uniq(find_latests(load_rpms(rpmlist)))
    logging.debug("Loaded %d unique rpms from %s" % (len(rpms), rpmlist))

    logging.debug(
        "Trying to connect to %s@%s" % (options.user, options.server)
    )
    (srv, sid) = connect(options.server, options.user, options.passwd)

    ref_rpms = uniq(concat(
        [p for p in
            packages_in_channel_g(srv, sid, c, options.latest)
        ] for c in options.channels
    ))
    logging.debug(
        "Got %d unique rpms in channels %s from RHNS" % \
            (len(ref_rpms), options.channels)
    )
 
    for us in find_updates_g(ref_rpms, rpms):
        for u in uniq(us):
            print options.format % u

    srv.auth.logout(sid)


if __name__ == '__main__':
    main()

# vim:sw=4:ts=4:expandtab:
