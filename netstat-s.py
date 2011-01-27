#! /usr/bin/python
# a python version of 'netstat -s'
#
# Author: Satoru SATOH <ssato@redhat.com>
# Licnese: GPLv2+
#
import itertools
import logging
import os
import sys

# from net-tools/statistics.c:
MSG_MAPS = {
    "Ip:" : {
        "Forwarding": "Forwarding is %s",
        "DefaultTTL": "Default TTL is %s",
        "InReceives": "%s total packets received",
        "InHdrErrors": "%s with invalid headers",
        "InAddrErrors": "%s with invalid addresses",
        "ForwDatagrams": "%s forwarded",
        "InUnknownProtos": "%s with unknown protocol",
        "InDiscards": "%s incoming packets discarded",
        "InDelivers": "%s incoming packets delivered",
        "OutRequests": "%s requests sent out",
        "OutDiscards": "%s outgoing packets dropped",
        "OutNoRoutes": "%s dropped because of missing route",
        "ReasmTimeout": "%s fragments dropped after timeout",
        "ReasmReqds": "%s reassemblies required",
        "ReasmOKs": "%s packets reassembled ok",
        "ReasmFails": "%s packet reassembles failed",
        "FragOKs": "%s fragments received ok",
        "FragFails": "%s fragments failed",
        "FragCreates": "%s fragments created",
    },
    "Icmp:": {
        "InMsgs": "%s ICMP messages received",
        "InErrors": "%s input ICMP message failed.",
        "InDestUnreachs": "destination unreachable: %s",
        "InTimeExcds": "timeout in transit: %s",
        "InParmProbs": "wrong parameters: %s",
        "InSrcQuenchs": "source quenches: %s",
        "InRedirects": "redirects: %s",
        "InEchos": "echo requests: %s",
        "InEchoReps": "echo replies: %s",
        "InTimestamps": "timestamp request: %s",
        "InTimestampReps": "timestamp reply: %s",
        "InAddrMasks": "address mask request: %s",
        "InAddrMaskReps": "address mask replies: %s",
        "OutMsgs": "%s ICMP messages sent",
        "OutErrors": "%s ICMP messages failed",
        "OutDestUnreachs": "destination unreachable: %s",
        "OutTimeExcds": "time exceeded: %s",
        "OutParmProbs": "wrong parameters: %s",
        "OutSrcQuenchs": "source quench: %s",
        "OutRedirects": "redirect: %s",
        "OutEchos": "echo request: %s",
        "OutEchoReps": "echo replies: %s",
        "OutTimestamps": "timestamp requests: %s",
        "OutTimestampReps": "timestamp replies: %s",
        "OutAddrMasks": "address mask requests: %s",
        "OutAddrMaskReps": "address mask replies: %s",
    },
    "Tcp:": {
        "RtoAlgorithm": "RTO algorithm is %s",
        "RtoMin": "",
        "RtoMax": "",
        "MaxConn": "",
        "ActiveOpens": "%s active connections openings",
        "PassiveOpens": "%s passive connection openings",
        "AttemptFails": "%s failed connection attempts",
        "EstabResets": "%s connection resets received",
        "CurrEstab": "%s connections established",
        "InSegs": "%s segments received",
        "OutSegs": "%s segments send out",
        "RetransSegs": "%s segments retransmited",
        "InErrs": "%s bad segments received.",
        "OutRsts": "%s resets sent",
    },
    "Udp:": {
        "InDatagrams": "%s packets received",
        "NoPorts":"%s packets to unknown port received.",
        "InErrors": "%s packet receive errors",
        "OutDatagrams": "%s packets sent",
    },
    "IcmpMsg:": {},
    "UdpLite:": {},
    "TcpExt:": {
        "SyncookiesSent": "%s SYN cookies sent",
        "SyncookiesRecv": "%s SYN cookies received",
        "SyncookiesFailed": "%s invalid SYN cookies received",
        "EmbryonicRsts": "%s resets received for embryonic SYN_RECV sockets",
        "PruneCalled": "%s packets pruned from receive queue because of socket buffer overrun",
        "RcvPruned": "%s packets pruned from receive queue",
        "OfoPruned": "%s packets dropped from out-of-order queue because of socket buffer overrun",
        "OutOfWindowIcmps": "%s ICMP packets dropped because they were " "out-of-window",
        "LockDroppedIcmps": "%s ICMP packets dropped because" " socket was locked",
        "TW": "%s TCP sockets finished time wait in fast timer",
        "TWRecycled": "%s time wait sockets recycled by time stamp",
        "TWKilled": "%s TCP sockets finished time wait in slow timer",
        "PAWSPassive": "%s passive connections rejected because of time stamp",
        "PAWSActive": "%s active connections rejected because of " "time stamp",
        "PAWSEstab": "%s packets rejects in established connections because of timestamp",
        "DelayedACKs": "%s delayed acks sent",
        "DelayedACKLocked": "%s delayed acks further delayed because of locked socket",
        "DelayedACKLost": "Quick ack mode was activated %s times",
        "ListenOverflows": "%s times the listen queue of a socket overflowed",
        "ListenDrops": "%s SYNs to LISTEN sockets ignored",
        "TCPPrequeued": "%s packets directly queued to recvmsg prequeue.",
        "TCPDirectCopyFromBacklog": "%s packets directly received from backlog",
        "TCPDirectCopyFromPrequeue": "%s packets directly received from prequeue",
        "TCPPrequeueDropped": "%s packets dropped from prequeue",
        "TCPHPHits": "%s packets header predicted",
        "TCPHPHitsToUser": "%s packets header predicted and directly queued to user",
        "SockMallocOOM": "Ran %s times out of system memory during packet sending",
        "TCPPureAcks": "%s acknowledgments not containing data received",
        "TCPHPAcks": "%s predicted acknowledgments",
        "TCPRenoRecovery": "%s times recovered from packet loss due to fast retransmit",
        "TCPSackRecovery": "%s times recovered from packet loss due to SACK data",
        "TCPSACKReneging": "%s bad SACKs received",
        "TCPFACKReorder": "Detected reordering %s times using FACK",
        "TCPSACKReorder": "Detected reordering %s times using SACK",
        "TCPTSReorder": "Detected reordering %s times using time stamp",
        "TCPRenoReorder": "Detected reordering %s times using reno fast retransmit",
        "TCPFullUndo": "%s congestion windows fully recovered",
        "TCPPartialUndo": "%s congestion windows partially recovered using Hoe heuristic",
        "TCPDSackUndo": "%s congestion window recovered using DSACK",
        "TCPLossUndo": "%s congestion windows recovered after partial ack",
        "TCPLostRetransmits": "%s retransmits lost",
        "TCPRenoFailures":  "%s timeouts after reno fast retransmit",
        "TCPSackFailures":  "%s timeouts after SACK recovery",
        "TCPLossFailures":  "%s timeouts in loss state",
        "TCPFastRetrans": "%s fast retransmits",
        "TCPForwardRetrans": "%s forward retransmits",
        "TCPSlowStartRetrans": "%s retransmits in slow start",
        "TCPTimeouts": "%s other TCP timeouts",
        "TCPRenoRecoveryFailed": "%s reno fast retransmits failed",
        "TCPSackRecoveryFail": "%s sack retransmits failed",
        "TCPSchedulerFailed": "%s times receiver scheduled too late for direct processing",
        "TCPRcvCollapsed": "%s packets collapsed in receive queue due to low socket buffer",
    },
}



def pr(ys, mmaps=MSG_MAPS):
    key = ys[0][0]
    print key

    for y in ys[1:]:
        k,v = y
        f = mmaps.get(key, {}).get(k, False) or k + ": %s"
        #logging.warn("k=%s, v=%s, fmt=%s" % (k,v,f))
        print "\t" + f % v


def process_statfile(statfile):
    xss = [l.rstrip().split() for l in open(statfile).readlines() if l]
    return ([t for t in itertools.izip(*y)] for y in zip(xss[::2], xss[1::2]))


def main():
    sfs = ("/proc/net/snmp", "/proc/net/netstat", "/proc/net/sctp/snmp")

    # usage: $0 [PREFIX]
    if len(sys.argv) > 1:
         sfs = [os.path.join(sys.argv[1], p[1:]) for p in sfs]

    for f in sfs:
        if not os.path.exists(f):
            logging.warn("%s does not exist. skipping it..." % f)
            continue

        for ys in process_statfile(f):
            pr(ys)


if __name__ == '__main__':
    main()

