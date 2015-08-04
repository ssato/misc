#! /usr/bin/python
#
# Test UDP multicast communication between nodes.
#
# License: MIT
# Author: Satoru SATOH <ssato@redhat.com>
#
# Contributors:
#  * Eduardo Damato <edamato@redhat.com>: Idea and basic implementation of
#    client loop, timestamps and serial ids on every packets.
#
#
# NOTE: This is just an example script of multicast communication in python. It
# is not a product supported by Red Hat and intended for production use.
#
#
# Changelog:
#
# 2009-11-26 Initial public release
# 2010-03-08 Merged a patch from Eduardo-san: added a client loop, timestamps
#            and serial ids on every packet sent. 
# 2010-03-10 Added new option -i, --interval to set sending interval (client)
#            and make statistics output when exit (server)
#
# References:
#   * Demo/sockets/mcast.py in python dist.
#   * http://wiki.python.org/moin/UdpCommunication#Multicasting.3F
#

"""multicast.py - check sending / receiving UDP multicast messages

Usage: 

  Server side: python multicast.py -s [Options]
  Client side: python multicast.py [Options] MESSAGE


Example:

  server:

    [root@rhel-5-cluster-1 ~]# python /shared/multicast.py -s -I 192.168.52.51
    Wed, 10 Mar 2010 03:28:49 DEBUG    Bound: 192.168.52.51:5405
    Wed, 10 Mar 2010 03:28:49 DEBUG    Joined the multicast network: 229.192.0.1 on 192.168.52.51
    Wed, 10 Mar 2010 03:28:55 INFO     Received 'hello' (#1) from 192.168.52.52:57109, time=47.656414
    Wed, 10 Mar 2010 03:28:56 INFO     Received 'hello' (#1) from 192.168.52.51:40262, time=0.067191
    Wed, 10 Mar 2010 03:28:57 INFO     Received 'hello' (#2) from 192.168.52.52:57109, time=48.658023
    Wed, 10 Mar 2010 03:28:58 INFO     Received 'hello' (#2) from 192.168.52.51:40262, time=1.068889
    (snip)
    Wed, 10 Mar 2010 03:29:04 INFO     Received 'hello' (#8) from 192.168.52.52:57109, time=49.664041
    Wed, 10 Mar 2010 03:29:05 INFO     Received 'hello' (#1) from 192.168.52.51:59353, time=2.534864
    Wed, 10 Mar 2010 03:29:06 INFO     Received 'hello' (#2) from 192.168.52.51:59353, time=2.535737
    Wed, 10 Mar 2010 03:29:07 INFO     Received 'hello' (#9) from 192.168.52.52:57109, time=51.666567
    Wed, 10 Mar 2010 03:29:08 INFO     Received 'hello' (#10) from 192.168.52.52:57109, time=51.667432
    Wed, 10 Mar 2010 03:29:09 INFO     Received 'hello' (#3) from 192.168.52.51:59353, time=4.538297
    Wed, 10 Mar 2010 03:29:10 INFO     Received 'hello' (#11) from 192.168.52.52:57109, time=52.669158
    Wed, 10 Mar 2010 03:29:11 INFO     Received 'hello' (#12) from 192.168.52.52:57109, time=52.670007
    Wed, 10 Mar 2010 03:29:12 INFO     Received 'hello' (#14) from 192.168.52.52:57109, time=51.670842
    Wed, 10 Mar 2010 03:29:12 DEBUG    LOST segments! #13 from 192.168.52.52:57109
    Wed, 10 Mar 2010 03:29:13 INFO     Received 'hello' (#15) from 192.168.52.52:57109, time=51.671702
    Wed, 10 Mar 2010 03:29:14 INFO     Received 'hello' (#16) from 192.168.52.52:57109, time=51.672572
    Wed, 10 Mar 2010 03:29:15 INFO     Received 'hello' (#17) from 192.168.52.52:57109, time=51.673432
    ^C
    Wed, 10 Mar 2010 03:29:16 INFO     Exiting...
    Wed, 10 Mar 2010 03:29:16 INFO     192.168.52.51:40262: Received = 2, (maybe) Lost = 0
    Wed, 10 Mar 2010 03:29:16 INFO     192.168.52.51:59353: Received = 3, (maybe) Lost = 0
    Wed, 10 Mar 2010 03:29:16 INFO     192.168.52.52:57109: Received = 16, (maybe) Lost = 1
    Wed, 10 Mar 2010 03:29:16 DEBUG    Left the multicast network: 229.192.0.1 on 192.168.52.51
    [root@rhel-5-cluster-1 ~]#


  clients:

    [root@rhel-5-cluster-1 ~]# python /shared/multicast.py -I 192.168.52.51 -c 2 hello
    Wed, 10 Mar 2010 03:28:56 DEBUG    Joined the multicast network: 229.192.0.1 on 192.168.52.51
    Wed, 10 Mar 2010 03:28:56 INFO     Sent data: '000000001 1268159336.72 hello'
    Wed, 10 Mar 2010 03:28:57 INFO     Sent data: '000000002 1268159337.72 hello'
    Wed, 10 Mar 2010 03:28:57 DEBUG    Left the multicast network: 229.192.0.1 on 192.168.52.51
    [root@rhel-5-cluster-1 ~]# python /shared/multicast.py -I 192.168.52.51 -c 3 hello
    Wed, 10 Mar 2010 03:29:03 DEBUG    Joined the multicast network: 229.192.0.1 on 192.168.52.51
    Wed, 10 Mar 2010 03:29:03 INFO     Sent data: '000000001 1268159343.26 hello'
    Wed, 10 Mar 2010 03:29:04 INFO     Sent data: '000000002 1268159344.26 hello'
    Wed, 10 Mar 2010 03:29:05 INFO     Sent data: '000000003 1268159345.26 hello'
    Wed, 10 Mar 2010 03:29:05 DEBUG    Left the multicast network: 229.192.0.1 on 192.168.52.51
    [root@rhel-5-cluster-1 ~]#

    [root@rhel-5-cluster-2 ~]# python /shared/multicast.py -I 192.168.52.52 hello
    Wed, 10 Mar 2010 03:28:08 DEBUG    Joined the multicast network: 229.192.0.1 on 192.168.52.52
    Wed, 10 Mar 2010 03:28:08 INFO     Sent data: '000000001 1268159288.13 hello'
    Wed, 10 Mar 2010 03:28:09 INFO     Sent data: '000000002 1268159289.13 hello'
    (snip)
    Wed, 10 Mar 2010 03:28:33 INFO     Sent data: '000000026 1268159313.13 hello'
    Wed, 10 Mar 2010 03:28:34 INFO     Sent data: '000000027 1268159314.13 hello'
    ^C
    Wed, 10 Mar 2010 03:28:34 INFO     Exiting...
    Wed, 10 Mar 2010 03:28:34 DEBUG    Left the multicast network: 229.192.0.1 on 192.168.52.52
    [root@rhel-5-cluster-2 ~]#


Notes:

 * It's always better to specify the interface (address) for multicast
   communication explicitly, I think.

 * If you're running kvm nodes inside the NAT-ed network, you maybe have to
   set ttl to 2.

"""


import logging
import optparse
import socket
import struct
import sys
import time
import traceback


IP4_ADDR_ANY = '0.0.0.0'  # socket.INADDR_ANY
DATA_FMT = "%(seq)09d %(time)s %(data)s"



class MulticastSocket(socket.socket):
    def __init__(self, grp_addr, if_addr=IP4_ADDR_ANY, ttl=1):
        """
        @param  grp_addr:  Multicast network address
        @param  if_addr:   Interface address to use for.
        @param  ttl:       time to live.

        SEE ALSO: getsockopt(2), ip(7)
        """
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        self.mreq = socket.inet_aton(grp_addr) + socket.inet_aton(if_addr)

        if if_addr != IP4_ADDR_ANY:
            # Specify the interface to send packets.
            self.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(if_addr))
        else:
            # The interface to send packets will be selected by kernel
            # automatically.
            pass

        if ttl > 1:
            self.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack('b', ttl))

        self.grp_addr = grp_addr
        self.if_addr = if_addr

    def __del__(self):
        self.leave()
        self.close()

    def join(self):
        # FIXME: Check the return value of setsockopt.
        #
        # Unfortunately, the following code does not work because
        # socket.getsockopt will return None.
        #
        #if self.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, self.mreq) != 0:
        #    logging.error("Could not join '%s' on '%s:%d'" % (grp_addr, if_addr, port))
        self.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, self.mreq)
        logging.debug("Joined the multicast network: %s on %s" % (self.grp_addr, self.if_addr))

    def leave(self):
        # FIXME: Likewise (see above note).
        self.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP, self.mreq)
        logging.debug("Left the multicast network: %s on %s" % (self.grp_addr, self.if_addr))



class MulticastServer(object):
    def __init__(self, grp_addr, port, if_addr=IP4_ADDR_ANY, ttl=1, reuse=False):
        self.sock = MulticastSocket(grp_addr, if_addr, ttl)

        if reuse:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if hasattr(socket, "SO_REUSEPORT"):
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        self.sock.bind(('', port))
        logging.debug("Bound: %s:%d" % (self.sock.if_addr, port))

        self.sock.join()

    def __del__(self):
        del self.sock

    def dump_stat(self, packets):
        for cli, ids in packets.iteritems():
            cli_s = "%s:%d" % cli
            rcvd = ["#%d" % id for id in ids]
            lost = ["#%d" % id for id in range(1, max(ids)) if id not in ids]
            (rcvd_n, lost_n) = (len(rcvd), len(lost))
            #(rcvd_s, lost_s) = (", ".join(rcvd), ", ".join(lost))

            logging.info("%s: Received = %d, (maybe) Lost = %d" % (cli_s, rcvd_n, lost_n))

    def loop(self, interval=1):
        packets = dict()

        try:
            while True:
                (segment, (ip4_addr, port)) = self.sock.recvfrom(1024)

                if not segment:
                    logging.info("Exiting as received an empty packet...")
                    sys.exit(0)

                tup = segment.split()
                if len(tup) < 3:
                    logging.info("Exiting as received an empty data packet...")
                    sys.exit(0)

                # @see DATA_FMT
                (id, time_sent, data) = tup
                try:
                    id = int(id)
                    time_sent = float(time_sent)
                except ValueError:
                    logging.warn("Unexpected formatted data was received. Skip it.")
                    continue

                last_ids = packets.get((ip4_addr, port), [])
                if last_ids:
                    last_id = last_ids[-1]
                else:
                    last_id = 0
                    packets[(ip4_addr, port)] = []

                delta = time.time() - time_sent
                from_s = "from %s:%d" % (ip4_addr, port)

                logging.info("Received '%s' (#%d) %s, time=%f" % (data, id, from_s, delta))

                if id < last_id:
                    logging.debug("Inversion! #%d %s is younger than last one (#%d)." % (id, from_s, last_id))
                elif id == last_id:
                    logging.debug("DUP segment! #%d %s" % (id, from_s))
                else:
                    if id > (last_id + 1):
                        last_received = packets[(ip4_addr, port)]
                        losts = ["#%d" % i for i in range(last_id + 1, id) if i not in last_received]
                        losts_s = ", ".join(losts)
                        logging.debug("LOST segments! %s %s" % (losts_s, from_s))

                packets[(ip4_addr, port)].append(id)

                # TODO: Send back to client.
                #ssize = self.sock.sendto(segment, (ip4_addr, port))
                #if ssize < len(segment):
                #    logging.warn("Failed to send back to the client: %s (port: %d)" % (ip4_addr, port))

                time.sleep(interval)

        except (KeyboardInterrupt, SystemExit):
            logging.info("Exiting...")
            self.dump_stat(packets)
        except:
            traceback.print_exc()

    def run(self):
        self.loop()



class MulticastClient(object):
    def __init__(self, grp_addr, port, if_addr=IP4_ADDR_ANY, ttl=1, datafmt=DATA_FMT):
        self.sock = MulticastSocket(grp_addr, if_addr, ttl)
        self.grp_addr = grp_addr
        self.port = port
        self.datafmt = datafmt

        if if_addr != IP4_ADDR_ANY:
            self.sock.join() # I think this is necessary for such cases.

    def loop(self, data, count=0, interval=1):
        try:
            seq = 1

            while True:
                segment = self.datafmt % {'seq':seq, 'time':time.time(), 'data': data}
                ssize = self.sock.sendto(segment, (self.grp_addr, self.port))

                if ssize < len(segment):
                    logging.warn("Failed to send: '%s'" % segment)
                else:
                    logging.info("Sent data: '%s'" % segment)

                if count > 0 and seq >= count:
                    return ssize == len(segment)

                seq += 1
                time.sleep(interval)

        except (KeyboardInterrupt, SystemExit):
            logging.info("Exiting...")
        except:
            traceback.print_exc()



def opts_parser(mcast_addr_default, port_default, **kwargs):
    p = optparse.OptionParser("%prog [OPTION ...]\n\n"
        "  Server mode: %prog [OPTION ...],\n"
        "  Client mode: %prog [OPTION ...] [DATA_TO_SEND]"
    )

    p.add_option('-s', '--server', action="store_true", default=False,
        help='Server mode. [Default: client mode]')

    # options in jgroup's test code:
    # common: bind_addr, mcast_addr, port, (receive|send)_on_all_interfaces
    # server (receiver): no unique options
    # client (sender): ttl
    p.add_option('-M', '--mcast_addr', default=mcast_addr_default,
        dest='mcast_addr', help='Multicast network address to join/sendto. [%default]')
    p.add_option('-I', '--if_addr', default=IP4_ADDR_ANY, dest='if_addr',
        help='Interface address to listen on. [IPv4 ADDR_ANY, i.e. automatically selected]')
    p.add_option('-p', '--port', default=port_default, type="int",
        help='Port to listen on/connect. [%default]')
    p.add_option('-t', '--ttl', default=1, type="int", help='Time-to-live for multicast packets [%default]')

    p.add_option('-q', '--quiet', action="store_true", help="Quiet mode; suppress debug message")

    sog = optparse.OptionGroup(p, "Options for server mode")
    sog.add_option('-r', '--reuse', action="store_true", default=False, help='Reuse socket? [no]')
    p.add_option_group(sog)

    cog = optparse.OptionGroup(p, "Options for client mode")
    cog.add_option('-c', '--count', type="int", default=0,
        help="Stop after sending COUNT packets. By default, it will send packets forever [%default].")
    cog.add_option('-i', '--interval', type="int", default=1,
        help="Wait  interval  seconds between sending each packet. [%default].")
    p.add_option_group(cog)

    return p


def main():
    """Entry point.
    """
    logformat = '%(asctime)s %(levelname)-8s %(message)s'
    logdatefmt = '%a, %d %b %Y %H:%M:%S'

    mcast_addr = '229.192.0.1'  # cman default; cman(5)
    port = 5405                 # likewise

    parser = opts_parser(mcast_addr, port)
    (options, args) = parser.parse_args()

    if options.quiet:
        loglevel = logging.INFO
    else:
        loglevel = logging.DEBUG

    try:
        # logging.basicConfig() in python older than 2.4 cannot handle kwargs,
        # then exception 'TypeError' will be thrown.
        logging.basicConfig(level=loglevel, format=logformat, datefmt=logdatefmt)
    except TypeError:
        # To keep backward compatibility. See above comment also.
        logging.getLogger().setLevel(loglevel)

    if options.server:
        srv = MulticastServer(options.mcast_addr,
                              options.port,
                              options.if_addr,
                              options.ttl,
                              options.reuse)
        srv.run()
    else:
        try:
            data = (len(args) > 0 and args[0] or raw_input('Type any to sendto > '))
        except EOFError:
            sys.exit(0)

        cli = MulticastClient(options.mcast_addr,
                              options.port,
                              options.if_addr,
                              options.ttl)
        cli.loop(data, options.count, options.interval)


if __name__ == '__main__':
    main()

# vim: set sw=4 ts=4 et ai si sm:
