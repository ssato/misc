#! /usr/bin/python
# 
# gktool.py - Set or search for the secret from keyring
#
#
# Copyright (c) 2008, 2009 Satoru SATOH <satoru.satoh@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# @see http://library.gnome.org/devel/gnome-keyring/
#

"""
Usage: $0 [Options...]



Advanced example:

It enables mutt to get mail account passwords in the gnome-keyring database.
For example, there is the following line in my muttrc:

  source "~/.mutt/gksearch.py -f 'set imap_pass = \"%(password)s\"' \
    -t network -a user:ssato,server:xxx.xxxxx.com,protocol:imaps|"
"""


import getpass
import glib
import logging
import optparse
import os.path
import sys



try:
    import gnomekeyring as gk
except ImportError:
    raise RuntimeError("Python gnome-keyring module is not installed on your system.")



glib.set_application_name('gktool.py')



def parse_kvpairs(s):
    """Construct and returns a dict ({key: val, ....}) from given string in
    format such like "key0:val0[,key1:val1,...]".

    >>> parse_kvpairs("key0:val0,key1:val1,key2:val2")
    {'key0': 'val0', 'key1': 'val1', 'key2': 'val2'}
    >>> parse_kvpairs("key0:val0")
    {'key0': 'val0'}
    >>> parse_kvpairs("")
    {}
    >>> parse_kvpairs(":")
    {}
    >>> parse_kvpairs("key0")
    {}
    >>> parse_kvpairs("key0:")
    {}
    >>> parse_kvpairs(":val0")
    {}
    >>> parse_kvpairs("key0:,")
    {}
    """
    try:
        return dict([(k,v) for k,v in [x.split(':') for x in s.split(',')] if k and v])
    except ValueError:
        return {}



class SecretManager(object):
    """Generic secret manager.
    """
    type = gk.ITEM_GENERIC_SECRET

    def check_attributes(self, attrs):
        assert isinstance(attrs, dict), " attrs: %s" % str(attrs)
        assert attrs != {}, " attrs is an empty dict: {}"

    def create(self, name, attrs, secret, keyring, force=False):
        """
        @return  secret ID # or -1 (error)
        """
        self.check_attributes(attrs)

        if not force and self.find(attrs, True) != []:
            logging.warn(" Secret already exists for display_name = '%s', attrs = '%s'" % (name, str(attrs)))
            return -1

        return gk.item_create_sync(keyring, self.type, name, attrs, secret, force)

    def find(self, attrs, single=False):
        """Search for secret with $attrs in all of the keyrings.
        """
        self.check_attributes(attrs)

        results = []
        try:
            for k in gk.find_items_sync(self.type, attrs):
                x = {
                    'keyring': k.keyring,
                    'id': k.item_id,
                    'attributes': k.attributes,
                    'secret': k.secret,
                }
                try:
                    x['display_name'] = gk.item_get_info_sync(k.keyring, k.item_id).get_display_name()
                except gk.DeniedError:
                    raise  # should not happen.

                logging.info(" x = %s" % str(x))
                results.append(x)

                if single:
                    return results

        except gk.NoMatchError:
            pass
        except:
            raise

        return results



class NetworkSecretManager(SecretManager):
    """Network Secret Manager
    """
    type = gk.ITEM_NETWORK_PASSWORD

    attributes = {
        'user':None, 'domain':None, 'server':None, 'object':None, 
        'protocol':None, 'authtype':None, 'port': 0, 
    }

    def check_attributes(self, attrs):
        return all([(key in attrs.keys()) for key in self.attributes.keys()])

    def del_empty_attributes(self, attrs):
        """
        >>> NetworkSecretManager().del_empty_attributes({'test':1, 'b':2, 'c':None, 'd':0})
        {'b': 2, 'test': 1}
        """
        return dict(((k,v) for k,v in attrs.iteritems() if v is not None and v != 0))

    def create(self, name, attrs, secret, keyring=gk.get_default_keyring_sync(), force=False):
        self.check_attributes(attrs)
        attrs2 = self.del_empty_attributes(attrs)

        if not force and self.find(attrs, True) != []:
            logging.warn(" Secret already exists for display_name = '%s', attrs = '%s'" % (name, str(attrs)))
            return -1

        return gk.set_network_password_sync(keyring, password=secret, **attrs2)

    def find(self, attrs, single=False):
        self.check_attributes(attrs)

        results = []
        try:
            for x in gk.find_network_password_sync(**attrs):
                # x == {'keyring:..., 'item_id':..., 'secret':..., ...}
                x['secret'] = x.get('password')
                x['id'] = x.get('item_id')
                try:
                    x['display_name'] = gk.item_get_info_sync(x['keyring'], x['id']).get_display_name()
                except gk.DeniedError:
                    raise  # should not happen.

                logging.info(" x = %s" % str(x))
                results.append(x)

                if single:
                    return results

        except gk.NoMatchError:
            pass
        except:
            raise

        return results




def option_parser():
    parser = optparse.OptionParser(version='%prog 0.1', usage='%prog [OPTION ...] CMD\n\nCommands = [get]|set')
    parser.add_option("-a", "--attrs",
        help="Comma separated pairs of attrribute and its value for secret in format attr1:val1[,attr2:val2,attr3:val3]")
    parser.add_option('-k', '--keyring', default=gk.get_default_keyring_sync(), help='Specify keyring to add new secret.')
    parser.add_option("-t", "--type",
        help="Secret type; generic (default) or network.\n\tNOTE: if type 'network' is given, you must specify some of attributes;\n\tuser, domain, server, object, protocol, authtype, port.")
    parser.add_option("-v", "--verbose", action="store_true", help="Verbose mode")

    gog = optparse.OptionGroup(parser, "Options for 'get' command")
    default_fmt = "#%(id)d: %(display_name)s in keyring %(keyring)s"
    gog.add_option("-f", "--format", default=default_fmt,
        help="Output result in given python string style format. \n\t" + 
            r'[Default: "#%(id)d: %(display_name)s in keyring %(keyring)s"]')
    gog.add_option("-S", "--single", action="store_true", help="Print the first secret only even if multiple secrets are found.")
    parser.add_option_group(gog)

    sog = optparse.OptionGroup(parser, "Options for 'set' command")
    sog.add_option("", "--name", help="Specify display_name for new secret to create. [MUST]")
    sog.add_option("", "--secret", default=False,
        help="Specify secret (password). NOTE: this tool will ask you about it and it's not necessaary to specify password.")
    parser.add_option_group(sog)

    return parser



def main():
    prog = os.path.basename(sys.argv[0]) or 'gktool.py'
    #glib.set_application_name(prog)

    (GET,SET) = (0,1)

    # defaults:
    verbose = False
    attrs = {}
    cmd = GET
    mngr = SecretManager()
    loglevel = logging.WARN

    parser = option_parser()
    (options, args) = parser.parse_args()

    if options.verbose:
        loglevel = logging.INFO

    logging.basicConfig(level=loglevel)

    if options.type and options.type == 'network':
        mngr = NetworkSecretManager()

    if len(args) < 1 or args[0] not in ('get', 'set'):
        parser.print_usage()
        sys.exit(-1)
    else:
        if args[0] == 'set':
            cmd = SET

    if options.attrs:
        attrs = parse_kvpairs(options.attrs)
        logging.info(" attrs = %s" % attrs)
    else:
        logging.error(" Attributes must be specified with --attrs option.")
        sys.exit(-1)

    if cmd == GET:
        results = mngr.find(attrs, options.single)

        for res in results:
            print >> sys.stdout, options.format % res
    else:
        if not options.name:
            print >> sys.stderr, " You must specify the display name for this secret!"
            sys.exit(-1)

        secret = options.secret
        if not secret:
            secret = getpass.getpass('Enter password > ')
            secret2 = getpass.getpass('Re-enter password to confirm > ')

            if secret != secret2:
                print >> sys.stderr, "The passwords' pair does not match!"
                sys.exit(-1)

        mngr.create(options.name, attrs, secret, options.keyring, force=False)


    exit(0)


if __name__ == '__main__':
    main()

# vim: set sw=4 ts=4 et ai si sm:
