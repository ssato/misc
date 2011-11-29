#! /usr/bin/python
#
# Copyright (C) 2011 Red Hat, Inc.
# Red Hat Author(s): Satoru SATOH <ssato@redhat.com>
#
# License: MIT
#
from SimpleXMLRPCServer import SimpleXMLRPCServer

import libvirt
import logging
import optparse
import sys
import xmlrpclib


HOSTNAME = "localhost"
PORT = 8080
URI = "http://%s:%d" % (HOSTNAME, PORT)


class LibvirtXMLRpcServer(object):

    def __init__(self, uri=None, host=HOSTNAME, port=PORT, all=False):
        """
        :param uri: Libvirt connection URI. see virsh(1) also.
        :param host: Host in which this server instance runs
        :param port: Listening port
        :param all: If True, all methods of libvirt connection object will be
                    registered and exported to clients.
        """
        self._server = SimpleXMLRPCServer((host, port))
        self._conn = libvirt.open(uri)

        if all:
            self.register_instance(self._conn)
        else:
            self.register_functions(self._conn)

        self._server.register_introspection_functions()

    def run(self):
        try:
            logging.info("Starting. (Exit with '^C')")
            self._server.serve_forever()

        except KeyboardInterrupt:
            logging.info("Exiting ...")
            self._server.shutdown()

    def register_instance(self, conn):
        self._server.register_instance(conn)

    def register_functions(self, conn):
        for fn in dir(conn):
            f = getattr(conn, fn)
            if f:
                self._server.register_function(f, fn)


class LibvirtXMLRpcClient(object):

    def __init__(self, uri, verbose=False):
        """
        :param uri: Connection URI, e.g. "http://localhost:8080".
        """
        self._uri = uri
        self._server = xmlrpclib.ServerProxy(
            uri, verbose=verbose, use_datetime=True
        )

    def call(self, api, *args):
        logging.debug(" Call: api=%s, args=%s" % (api, str(args)))

        try:
            f = getattr(self._server, api)
            return f(*args)

        except xmlrpclib.Fault, m:
            raise RuntimeError(
                "rpc: method '%s', args '%s'\nError message: %s" % \
                    (api, str(args), m)
            )


def main(argv=sys.argv):
    logging.basicConfig(format="%(asctime)s %(levelname)-6s %(message)s",
                        datefmt="%H:%M:%S",  # or "%Y-%m-%d %H:%M:%S",
                       )

    o = optparse.OptionParser("%prog [Options...] [RPC_API [Arguments...]]")

    o.add_option("-s", "--server", help="server mode", action="store_true")
    o.add_option("-v", "--verbose", help="verbose mode", action="store_true")

    sog = optparse.OptionGroup(o, "Server options")
    sog.add_option("-H", "--hostname", default=HOSTNAME,
        help="Server hostname [%default]",
    )
    sog.add_option("-p", "--port", default=PORT, type=int,
        help="Listening port [%default]",
    )
    sog.add_option("-A", "--all", action="store_true",
        help="Export all libvirt connection methods",
    )
    sog.add_option("", "--connect", default=None,
        help="Libvirt connection URI [None]",
    )
    o.add_option_group(sog)

    cog = optparse.OptionGroup(o, "Client options")
    cog.add_option("-u", "--uri", default=URI,
        help="Connection URI [%default]",
    )
    o.add_option_group(cog)

    (opts, args) = o.parse_args(argv[1:])

    logging.getLogger().setLevel(
        logging.INFO if opts.verbose else logging.WARN
    )

    if opts.server:
        s = LibvirtXMLRpcServer(
            opts.connect, opts.hostname, opts.port, opts.all
        )
        s.run()
    else:
        if not args:
            o.print_usage()
            sys.exit(-1)

        api = args[0]
        api_args = args[1:]

        c = LibvirtXMLRpcClient(opts.uri)
        res = c.call(api, *api_args)

        print res


if __name__ == '__main__':
    main()


# vim:sw=4 ts=4 et:
