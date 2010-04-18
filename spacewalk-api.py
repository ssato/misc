#! /usr/bin/python
#
# Like spacewalk-api, call Spacewalk/RHN RPC API from command line.
#
# Copyright (C) 2010 Satoru SATOH <satoru.satoh@gmail.com>
#
# License: GPLv2+ (see COPYING.GPLv2 for more details)
#

import ConfigParser as configparser
import getpass
import logging
import optparse
import os
import random
import re
import simplejson
import sys
import time
import xmlrpclib


PROTO = 'https'
TIMEOUT = 900
CONFIG = os.path.join(os.environ.get('HOME', '.'), '.spacewalk-api', 'config')



class RpcApi(object):
    def __init__(self, conn_params):
        """
        @conn_params  Connection parameters: server, userid, password, timeout, protocol.
        """
        self.url = "%(protocol)s://%(server)s/rpc/api" % conn_params
        self.userid = conn_params.get('userid')
        self.passwd = conn_params.get('password')
        self.timeout = conn_params.get('timeout')

        self.sid = False

    def login(self):
        self.server = xmlrpclib.ServerProxy(self.url)
        self.sid = self.server.auth.login(self.userid, self.passwd, self.timeout)

    def call(self, method_name, *args):
        try:
            if not self.sid:
                self.login()

            method = getattr(self.server, method_name)

            # wait a little bit to avoid DoS attack to the server.
            time.sleep(random.random())

            # Special cases which do not need session_id parameter:
            # api.{getVersion, systemVersion} and auth.login.
            if re.match(r'^(api.|proxy.|auth.login)', method_name):
                ret = method(*args)
            else:
                ret = method(self.sid, *args)

            return ret

        except xmlrpclib.Fault, m:
            raise RuntimeError("rpc: method '%s', args '%s'\nError message: %s" % (method_name, str(args), m))



def __parse(arg):
    """
    >>> __parse('1234567')
    1234567
    >>> __parse('abcXYZ012')
    'abcXYZ012'
    >>> __parse('{"channelLabel": "foo-i386-5"}')
    {'channelLabel': 'foo-i386-5'}
    """
    try:
        if re.match(r'[1-9]\d*', arg):
            return int(arg)
        elif re.match(r'{.*}', arg):
            return eval(arg)
        else:
            return str(arg)

    except ValueError:
        return str(arg)


def parse_rpc_args(args, arg_sep=','):
    """
    Simple JSON-like expression parser.

    @args     options.args :: string
    @return   rpc arg objects, [arg] :: [string]

    >>> parse_rpc_args('1234567')
    [1234567]
    >>> parse_rpc_args('abcXYZ012')
    ['abcXYZ012']
    >>> parse_rpc_args('{"channelLabel": "foo-i386-5"}')
    [{'channelLabel': 'foo-i386-5'}]
    >>> parse_rpc_args('1234567,abcXYZ012,{"channelLabel": "foo-i386-5"}')
    [1234567, 'abcXYZ012', {'channelLabel': 'foo-i386-5'}]
    >>> parse_rpc_args('[1234567,"abcXYZ012",{"channelLabel": "foo-i386-5"}]')
    [1234567, 'abcXYZ012', {'channelLabel': 'foo-i386-5'}]
    """
    ret = []

    try:
        x = simplejson.loads(args)
        if isinstance(x, list):
            ret = x
        else:
            ret = [x]

    except ValueError:
        ret = [__parse(a) for a in args.split(arg_sep)]

    return ret


def resuls_to_str(results, human_readable=True):
    """
    >>> resuls_to_str([123, 'abc', {'x':'yz'}], False)
    '[123, "abc", {"x": "yz"}]'
    >>> resuls_to_str([123, 'abc', {'x':'yz'}])
    '[\\n  123, \\n  "abc", \\n  {\\n    "x": "yz"\\n  }\\n]'
    """
    indent = (human_readable and 2 or 0)
    return simplejson.dumps(results, ensure_ascii=False, indent=indent)


def init_config_with_configfile(config_file, profile=""):
    """
    @config_file  Configuration file path, ex. '~/.spacewalk-api/config'.
    """
    (server,userid,password,timeout,protocol) = ('', '', '', TIMEOUT, PROTO)

    # expand '~/'
    if '~' in config_file:
        config_file = os.path.expanduser(config_file)

    logging.debug(" config_file = %s" % config_file)

    cp = configparser.SafeConfigParser()

    try:
        cp.read(config_file)

        if profile and cp.has_section(profile):
            sect = profile
        else:
            sect = 'DEFAULT'
        logging.debug(" profile = '%s'" % profile)

        server = cp.get(sect, 'server')
        userid = cp.get(sect, 'userid')
        password = cp.get(sect, 'password')
        timeout = int(cp.get(sect, 'timeout'))
        protocol = cp.get(sect, 'protocol')

    except configparser.NoOptionError:
        raise

    return {
        'server': server,
        'userid': userid,
        'password': password,
        'timeout': timeout,
        'protocol': protocol
    }


def init_config_with_options(config, options):
    """
    @config   config parameters dict: {'server':, 'userid':, ...}
    @options  optparse.Options
    """
    server = config.get('server') or (options.server or raw_input('Enter server name > '))
    userid = config.get('userid') or (options.userid or raw_input('Enter user ID > '))
    password = config.get('password') or (options.password or getpass.getpass('Enter your password > '))
    timeout = config.get('timeout') or ((options.timeout and options.timeout != TIMEOUT) and options.timeout or TIMEOUT)
    protocol = config.get('protocol') or ((options.protocol and options.protocol != PROTO) and options.protocol or PROTO)

    return {'server':server, 'userid':userid, 'password':password, 'timeout':timeout, 'protocol':protocol}


def init_config(options):
    conf = init_config_with_configfile(options.config, options.profile)
    conf = init_config_with_options(conf, options)

    return conf


def option_parser(cmd=sys.argv[0]):
    p = optparse.OptionParser("""%(cmd)s [OPTION ...] RPC_STRING

Examples:
  %(cmd)s --args=10821 packages.listDependencies 
  %(cmd)s -P rhn --args=rhel-x86_64-server-vt-5 channel.software.getDetails
  %(cmd)s -C /tmp/s.cfg --args=rhel-x86_64-server-vt-5,guest channel.software.isUserSubscribable
  %(cmd)s --args="rhel-i386-server-5","2010-04-01 08:00:00" channel.software.listAllPackages
  %(cmd)s --args='["rhel-i386-server-5","2010-04-01 08:00:00"]' channel.software.listAllPackages
  %(cmd)s --args=100010021 --format "%%(hostname)s %%(description)s" system.getDetails
  %(cmd)s --format "%%(label)s" channel.listSoftwareChannels""" \
        % {'cmd': cmd}
    )

    p.add_option('-s', '--server', help='Spacewalk/RHN server hostname.')
    p.add_option('-u', '--userid', help='Spacewalk/RHN login user id')
    p.add_option('-p', '--password', help='Spacewalk/RHN Login password')
    p.add_option('-t', '--timeout', help='Session timeout in sec [%default]', default=TIMEOUT)
    p.add_option('',   '--protocol', help='RHN server protocol.', default="https")
    p.add_option('-C', '--config', help='Config file path [%default]', default=CONFIG)
    p.add_option('-P', '--profile', help='Connection profile name', default=False)
    p.add_option('-o', '--output', help="output file [default: stdout]")
    p.add_option('',   '--format', help="output format", default=False)
    p.add_option('-v', '--verbose', help='verbose mode', default=0, action="count")

    p.add_option('-T', '--test', help='Test mode', default=False, action="store_true")

    p.add_option('', '--args', default="",
        help='Comma separated api arguments other than session id (in str or JSON expression) [empty]')

    return p


def main(argv):
    rpc_args = False
    loglevel = logging.WARN
    out = sys.stdout

    parser = option_parser()
    (options, args) = parser.parse_args(argv[1:])

    if options.test:
        test()

    if options.verbose > 0:
        loglevel = logging.INFO

        if options.verbose > 1:
            loglevel = logging.DEBUG

    logging.basicConfig(level=loglevel)

    if options.output:
        out = open(options.output, 'w')

    if len(args) == 0:
        parser.print_usage()
        return 0

    rpc_cmd = [args[0]]
    logging.debug(" api = '%s'" % rpc_cmd[0])

    if options.args:
        rpc_args = parse_rpc_args(options.args)
        logging.debug(" rpc args = %s" % str(rpc_args))
        rpc_cmd += rpc_args

    conn_params = init_config(options)

    rapi = RpcApi(conn_params)
    rapi.login()

    xs = rapi.call(*rpc_cmd)

    # TODO: clean up this ugly and complex part.
    if isinstance(xs, list):
        if options.format:
            for x in xs:
                print >> out, options.format % x
        else:
            print >> out, resuls_to_str(xs)
    else:
        if options.format:
            print >> out, options.format % xs
        else:
            print >> out, resuls_to_str(xs)

    return 0


def test():
    import doctest
    doctest.testmod(verbose=True)
    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv)

# vim: set sw=4 ts=4 expandtab:
