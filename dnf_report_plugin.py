# report.py
# DNF Plugin to report summary of RPMs to install, update and remove.
#
# It implicitly assume the come back of --enableplugin option to dnf although
# it was removed as 'it's questionalbe use':
# http://dnf.readthedocs.io/en/latest/cli_vs_yum.html#enableplugin-not-recognized
#
# Copyright (C) 2016 Satoru SATOH <satoru.satoh@gmail.com>
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
"""DNF Plugin to report summary of RPMs to install, update and remove.
"""
from __future__ import absolute_import
from __future__ import unicode_literals

import dnf
import json
import logging
import operator
import uuid


PLUGIN_CONF = "report"
REPORT_PATH = "/tmp/dnf-report-{}.json"

LOGGER = logging.getLogger("dnf.plugin.report")

_TS_TYPES = "install upgrade reinstall erase downgrade fail".split()


# :see: dnf.cli.output._active_pkg
def _active_pkg(tsi):
    """
    Return the package from tsi that takes the active role in the transaction.

    :return: :class:`dnf.package.Package`
    """
    attr = "erased" if tsi.op_type == dnf.transaction.ERASE else "installed"
    return operator.attrgetter(attr)(tsi)


def _to_pkg(tsi):
    """
    :param tsi: An instance of :class:`dnf.transaction.TransactionItem`
    :return: A dict gives basic package info
    """
    apo = _active_pkg(tsi)
    return dict(naevr="%s.%s %s:%s-%s" % apo.pkgtup, name=apo.name,
                epoch=apo.epoch, version=apo.version, release=apo.release,
                arch=("noarch" if apo.arch is None else apo.arch),
                repoid=apo.from_repo)


# :see:`dnf.cli.output._make_lists`
def _make_lists(transaction, ts_types=None):
    """
    :param transaction: An instance of :class:`dnf.transaction.Transaction`
    """
    if ts_types is None:
        ts_types = _TS_TYPES

    pkgs = {t: [] for t in ts_types}

    for tsi in transaction:
        for ttype in ts_types:
            if tsi.op_type == getattr(dnf.transaction, ttype.upper(), None):
                pkgs[ttype].append(tsi)

    for ttype in ts_types:
        pkgs[ttype].sort(key=lambda tsi: str(tsi.active))

    return pkgs


class ReportPlugin(dnf.Plugin):
    """dnf.plugin.report class.
    """
    name = 'report'

    def __init__(self, base, cli):
        super(ReportPlugin, self).__init__(base, cli)
        self.base = base
        self.report_path = REPORT_PATH.format(str(uuid.uuid4()))

    def config(self):
        cfg = self.read_config(self.base.conf, PLUGIN_CONF)
        if cfg.has_section('main') and cfg.has_option('main', 'report_path'):
            report_path = cfg.get('main', 'report_path')
            self.report_path = report_path.format(str(uuid.uuid4()))

    def resolved_itr(self):
        """
        :see: dnf.cli.output.Output.list_transaction
        """
        ts_types = _TS_TYPES
        pkgs = _make_lists(self.base.transaction)
        for ttype in ts_types:
            yield (ttype, sorted((_to_pkg(tsi) for tsi in pkgs[ttype]),
                                 key=operator.itemgetter("naevr")))

    def resolved(self):
        """
        :see: dnf.cli.output.Output.list_transaction
        """
        pkgs = dict(self.resolved_itr())
        try:
            with open(self.report_path, 'w') as out:
                json.dump(pkgs, out, indent=2)
                LOGGER.info("Saved report as %s", self.report_path)
        except (OSError, IOError) as exc:
            LOGGER.warn("Something goes wrong with dnf.plugin.report: %s",
                        str(exc))

