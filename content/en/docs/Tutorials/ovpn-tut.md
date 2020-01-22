---
title: "Creating an encrypted IP tunnel"
author: "Dimitri Staessens"
date:  2019-08-31
#type:  page
draft: false
weight: 100
description: >
   This tutorial explains how to create an encrypted tunnel for IP traffic.
---

We recently added 256-bit ECDHE-AES encryption to Ouroboros (in the
_be_ branch). This tutorial shows how to create an *encrypted IP
tunnel* using the Ouroboros VPN (ovpn) tool, which exposes _tun_
interfaces to inject Internet Protocol traffic into an Ouroboros flow.

We'll first illustrate what's going on over an Ethernet loopback
adapter and then show how to create an encrypted tunnel between two
machines connected over an IP network.

{{<figure width="50%" src="/docs/tutorials/ovpn_tut.png">}}

We'll create an encrypted tunnel between IP addresses 127.0.0.3 /24
and 127.0.0.8 /24, as shown in the diagram above.

To run this tutorial, make sure that
[openssl](https://www.openssl.org) is installed on your machine(s) and
get the latest version of Ouroboros.

```bash
$ git clone https://ouroboros.rocks/git/ouroboros
$ cd ouroboros
$ mkdir build && cd build
$ cmake ..
$ make && sudo make install
```

# Encrypted tunnel over the loopback interface

Open a terminal window and start ouroboros (add --stdout to log to
stdout):

```bash
$ sudo irmd --stdout
```

To start, the network will just consist of the loopback adapter _lo_,
so we'll create a layer _my\_layer_ consisting of a single ipcp-eth-dix
named _dix_, register the name _my\_vpn_ for the ovpn server in
_my\_layer_, and bind the ovpn binary to that name.

```bash
$ irm ipcp bootstrap type eth-dix name dix layer my_layer dev lo
$ irm reg name my_vpn layer my_layer
$ irm bind program ovpn name my_vpn
```

We can now start an ovpn server on 127.0.0.3. This tool requires
superuser privileges as it creates a tun device.

```bash
$ sudo ovpn --ip 127.0.0.3 --mask 255.255.255.0
```

From another terminal, we can start an ovpn client to connect to the
server (which listens to the name _my\_vpn_) and pass the \-\-crypt
option to encrypt the tunnel:

```bash
$ sudo ovpn -n my_vpn -i 127.0.0.8 -m 255.255.255.0 --crypt
```

The ovpn tool now created two _tun_ interfaces attached to the
endpoints of the flow, and will act as an encrypted pipe for any
packets sent to that interface:

```bash
$ ip a
...
6: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UNKNOWN group default qlen 500
    link/none
    inet 127.0.0.3/24 scope host tun0
       valid_lft forever preferred_lft forever
    inet6 fe80::f81d:9038:9358:fdf4/64 scope link stable-privacy
       valid_lft forever preferred_lft forever
7: tun1: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UNKNOWN group default qlen 500
    link/none
    inet 127.0.0.8/24 scope host tun1
       valid_lft forever preferred_lft forever
    inet6 fe80::c58:ca40:5839:1e32/64 scope link stable-privacy
       valid_lft forever preferred_lft forever
```

To test the setup, we can tcpdump one of the _tun_ interfaces, and
send some ping traffic into the other _tun_ interface.
The encrypted traffic can be shown by tcpdump on the loopback interface.
Open two more terminals:

```bash
$ sudo tcpdump -i tun1
```

```bash
$ sudo tcpdump -i lo
```

From another terminal, send some pings into the other endpoint:

```bash
$ ping 10.10.10.1 -I tun0
```

The pings will timeout, but the tcpdump on the _tun1_ interface will
show the ping messages arriving:

```bash
$ sudo tcpdump -i tun1
[sudo] password for dstaesse:
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on tun1, link-type RAW (Raw IP), capture size 262144 bytes
13:35:20.229267 IP heteropoda > 10.10.10.1: ICMP echo request, id 3011, seq 1, length 64
13:35:21.234523 IP heteropoda > 10.10.10.1: ICMP echo request, id 3011, seq 2, length 64
13:35:22.247871 IP heteropoda > 10.10.10.1: ICMP echo request, id 3011, seq 3, length 64
```

While the tcpdump on the loopback shows the AES encrypted traffic that
is actually sent on the flow (and not visible to the legacy "network"
below:

```bash
$ sudo tcpdump -i lo
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on lo, link-type EN10MB (Ethernet), capture size 262144 bytes
13:35:20.229175 00:00:00:00:00:00 (oui Ethernet) > 00:00:00:00:00:00 (oui Ethernet), ethertype Unknown (0xa000), length 130:
        0x0000:  0041 0070 31f2 ae4c a03a 3e72 ec54 7ade  .A.p1..L.:>r.Tz.
        0x0010:  f2f3 1db4 39ce 3b62 d3ad c872 93b0 76c1  ....9.;b...r..v.
        0x0020:  4f76 b977 aa66 89c8 5c3c eedf 3085 8567  Ov.w.f..\<..0..g
        0x0030:  ed60 f224 14b2 72d1 6748 b04a 84dc e350  .`.$..r.gH.J...P
        0x0040:  d020 637a 6c2c 642a 214b dd83 7863 da35  ..czl,d*!K..xc.5
        0x0050:  28b0 0539 a06e 541f cd99 7dac 0832 e8fb  (..9.nT...}..2..
        0x0060:  9e2c de59 2318 12e0 68ee da44 3948 2c18  .,.Y#...h..D9H,.
        0x0070:  cd4c 58ed                                .LX.
13:35:21.234343 00:00:00:00:00:00 (oui Ethernet) > 00:00:00:00:00:00 (oui Ethernet), ethertype Unknown (0xa000), length 130:
        0x0000:  0041 0070 4295 e31d 05a7 f9b2 65a1 b454  .A.pB.......e..T
        0x0010:  5b6f 873f 0016 16ea 7c83 1f9b af4a 0ff2  [o.?....|....J..
        0x0020:  c2e6 4121 8bf9 1744 6650 8461 431e b2a0  ..A!...DfP.aC...
        0x0030:  94da f17d c557 b5ac 1e80 825c 7fd8 4532  ...}.W.....\..E2
        0x0040:  11b3 4c32 626c 46a5 b05b 0383 2aff 022a  ..L2blF..[..*..*
        0x0050:  e631 e736 a98e 9651 e017 7953 96a1 b959  .1.6...Q..yS...Y
        0x0060:  feac 9f5f 4b02 c454 7d31 e66f 2d19 3eaf  ..._K..T}1.o-.>.
        0x0070:  a5c8 d77f                                ....
13:35:22.247670 00:00:00:00:00:00 (oui Ethernet) > 00:00:00:00:00:00 (oui Ethernet), ethertype Unknown (0xa000), length 130:
        0x0000:  0041 0070 861e b65e 4227 5a42 0db4 8317  .A.p...^B'ZB....
        0x0010:  6a75 c0c1 94d0 de18 10e9 45f3 db96 997f  ju........E.....
        0x0020:  7461 2716 d9af 124d 0dd0 b6a0 e83b 95e7  ta'....M.....;..
        0x0030:  9e5f e4e6 068f d171 727d ba25 55c7 168b  ._.....qr}.%U...
        0x0040:  7aab 2d49 be53 1133 eab0 624a 5445 d665  z.-I.S.3..bJTE.e
        0x0050:  ca5c 7a28 9dfa 58c2 e2fd 715d 4b87 246a  .\z(..X...q]K.$j
        0x0060:  f54c b8c8 5040 1c1b aba1 6107 39e7 604b  .L..P@....a.9.`K
        0x0070:  5fb2 73ef
```

You can experiment with other small tools like nc (netcat) to monitor
both requests and responses.

# Encrypted tunnel between two IP hosts connected to the Internet

To create an encrypted tunnel between two Internet hosts, the same
procedure can be followed. The only difference is that we need to use
an ipcpd-udp on the end hosts connected to the ip address of the
machine, and on the client side, add the MD5 hash for that name to the
hosts file. The machines must have a port that is reachable from
outside, the default is 3435, but this can be configured using the
sport option.

On both machines (fill in the correct IP address):

```bash
irm i b t udp n udp l my_layer ip <address>
```

On the server machine, bind and register the ovpn tool as above:

```bash
$ irm reg name my_vpn layer my_layer
$ irm bind program ovpn name my_vpn
```

On the _client_ machine, add a DNS entry for the MD5 hash for "my_vpn"
with the server IP address to /etc/hosts:

```bash
$ cat /etc/hosts
# Static table lookup for hostnames.
# See hosts(5) for details.

...

<server_ip>    2694581a473adbf3d988f56c79953cae

```

and you should be able to create the ovpn tunnel as above.

On the server:

```bash
$ sudo ovpn --ip 127.0.0.3 --mask 255.255.255.0
```

And on the client:

```bash
$ sudo ovpn -n my_vpn -i 127.0.0.8 -m 255.255.255.0 --crypt
```
